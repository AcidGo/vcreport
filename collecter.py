import atexit

from config import *
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

class VCWorker(object):
    """连接 vCenter 进行登录认证，对内部资源做收集和管理操作。
    """
    # default variables
    use_ssl = False

    def __init__(self):
        self._vc_reset()

    def _vc_reset(self):
        self._args = {}
        self.service_instance = None
        self._atexit_func = None

    def login(self, **kwargs):
        """认证登录 vCenter，可以直接连接 ESXi，但不建议。

        Args:
            kwargs: 登录认证身份信息。
        """
        self._vc_reset()
        connect = SmartConnect if self.use_ssl is True else SmartConnectNoSSL
        try:
            service_instance = connect(**kwargs)
        except vim.fault.InvalidLogin as e:
            raise Exception(e.msg)
        
        self.service_instance = service_instance
        self._atexit_func = atexit.register(Disconnect, self.service_instance)
        self._args.update({k: v for k, v in kwargs.items() if k.lower() != "pwd"})

    def logout(self):
        """注销 vCenter 登录连接，手动关闭注册的回调函数。
        """
        if self.service_instance is None:
            Disconnect(self.service_instance)
        if self._atexit_func is not None:
            atexit.unregister(self._atexit_func)
            self._atexit_func = None

    def _get_container_view(self, obj_type, container=None):
        """从指定层次获取指定对象的搜寻视图。

        Args:
            obj_type: 检索对象的类型。
            container: 检索视图的容器范围。
        """
        if not container:
            container = self.service_instance.content.rootFolder

        view_ref = self.service_instance.content.viewManager.CreateContainerView(
            container=container,
            type=obj_type,
            recursive=True
        )
        return view_ref

    def _collect_properties(self, view_ref, obj_type, path_set=None):
        """通过传入的视图遍历指定对象的相关属性。

        Args:
            view_ref: 使用的视图参照对象。
            obj_type: 检索对象的类型。
            path_set: 检索属性类。
        Returns:
            props <vmodl.query.PropertyCollector.RetrieveResult>: 返回属性集合。
        """
        collector = self.service_instance.content.propertyCollector

        obj_spec = vmodl.query.PropertyCollector.ObjectSpec()
        obj_spec.obj = view_ref
        obj_spec.skip = True

        traversal_spec = vmodl.query.PropertyCollector.TraversalSpec()
        traversal_spec.name = 'traverseEntities'
        traversal_spec.path = 'view'
        traversal_spec.skip = False
        traversal_spec.type = view_ref.__class__
        obj_spec.selectSet = [traversal_spec]

        property_spec = vmodl.query.PropertyCollector.PropertySpec()
        property_spec.type = obj_type

        if not path_set:
            property_spec.all = True
        property_spec.pathSet = path_set

        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = [obj_spec]
        filter_spec.propSet = [property_spec]

        props = collector.RetrieveContents([filter_spec])

        return props

    def collect(self, v_obj_type, p_obj_type, path_set):
        """收集信息。
        """
        if not self.service_instance:
            raise Exception("unable to connect to host with supplied info")

        view = self._get_container_view(obj_type=v_obj_type)
        data = self._collect_properties(
            view_ref = view,
            obj_type = p_obj_type,
            path_set = path_set,
        )
        
        return data