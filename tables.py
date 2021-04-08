from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VCReport(Base):
    __tablename__ = "vcreport"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    create_time = Column(DateTime, nullable=False, comment="创建批次时间")
    alias = Column(String(100), nullable=False, comment="vCenter 人为设定别名")
    name = Column(String(100), nullable=False, comment="vCenter 系统内命名")
    flag = Column(String(100), nullable=True, comment="vSphere 标记")
    cluster_total = Column(Integer, nullable=False, comment="管理集群数量")
    host_total = Column(Integer, nullable=False, comment="管理接入的 ESXi 主机数量")
    host_running_total = Column(Integer, nullable=False, comment="正在运行的主机数量")
    cpu_total = Column(BigInteger, nullable=False, comment="CPU 资源总数，单位为物理核数")
    mem_total = Column(BigInteger, nullable=False, comment="内存资源总数，单位为 Byte")
    vm_total = Column(Integer, nullable=False, comment="虚拟机的总数量")
    vm_poweredoff_total = Column(Integer, nullable=False, comment="已关机的虚拟机的数量")
    ds_total = Column(Integer, nullable=False, comment="存储设备的总数量")
    ds_share_total = Column(Integer, nullable=False, comment="共享存储设备的总数量")

class DSReport(Base):
    __tablename__ = "dsreport"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    create_time = Column(DateTime, nullable=False, comment="创建批次时间")
    name = Column(String(100), nullable=False, comment="存储名称")
    vc_name = Column(String(100), comment="存储所在 vCenter 的名称")
    vc_alias = Column(String(100), comment="存储所在 vCenter 人为设定的别名")
    is_access = Column(Boolean, unique=False, comment="存储是否可访问的")
    is_multiple = Column(Boolean, unique=False, comment="存储是否为多路径访问")
    fs_type = Column(String(20), nullable=False, comment="存储所在 vCenter 的名称")
    space_total = Column(BigInteger, nullable=False, comment="存储的总容量，单位为 Byte")
    space_free = Column(BigInteger, nullable=False, comment="存储的可用容量， 单位为 Byte")
    space_uncommit = Column(BigInteger, nullable=False, comment="存储未提交分配容量， 单位为 Byte")
    host_num = Column(Integer, nullable=False, comment="挂载该存储的主机数量")
    vm_num = Column(Integer, nullable=False, comment="使用该存储的虚拟机数量")