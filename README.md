## vcreport

根据 VMware vSphere vCenter 资源视图做检索，持久化统计数据到后端存储，类似对 VirtualMachine 资源做统计并自动注册到监控系统的工具 [zabbix-vmrecord](https://github.com/AcidGo/zabbix-vmrecord)。

### 配置

主要配置文件为同级目录下的 config.py，主要为 sqlalchemy 存储端的地址和需要做遍历统计的 vCenter 查询用户信息。

```python
from urllib import parse
# vCenter 的的认证配置
VC_CONFIG_MAP = {
    "DC1-vCenter": {
        "host": "10.10.10.1",
        "user": "query",
        "pwd": "password",
    },
    "DC2-vCenter": {
        "host": "10.10.10.3",
        "user": "query",
        "pwd": "password",
    },
}
# 持久化的目标存储
REPORT_DB_DSN = "mysql+pymysql://user:{!s}@10.10.10.3:3306/db?charset=utf8".format(parse.unquote_plus("passw@rd"))
```

### 使用
配置正确的 config.py 和存储路径，执行 vcreport.py 即可。

目前提供的统计数据如下。

+ **vcreport**

| 属性                | 说明                         |
| ------------------- | ---------------------------- |
| alias               | vCenter 人为设定别名         |
| name                | vCenter 系统内命名           |
| flag                | vSphere 标记                 |
| cluster_total       | 管理集群数量                 |
| host_total          | 管理接入的 ESXi 主机数量     |
| host_running_total  | 正在运行的主机数量           |
| cpu_total           | CPU 资源总数，单位为物理核数 |
| mem_total           | 内存资源总数，单位为 Byte    |
| vm_total            | 虚拟机的总数量               |
| vm_poweredoff_total | 已关机的虚拟机的数量         |
| ds_total            | 存储设备的总数量             |
| ds_share_total      | 共享存储设备的总数量         |

+ **dsreport**

| 属性           | 说明                             |
| -------------- | -------------------------------- |
| name           | 存储名称                         |
| vc_name        | 存储所在 vCenter 的名称          |
| vc_alias       | 存储所在 vCenter 人为设定的别名  |
| is_access      | 存储是否可访问的                 |
| is_multiple    | 存储是否为多路径访问             |
| fs_type        | 存储所在 vCenter 的名称          |
| space_total    | 存储的总容量，单位为 Byte        |
| space_free     | 存储的可用容量， 单位为 Byte     |
| space_uncommit | 存储未提交分配容量， 单位为 Byte |
| host_num       | 挂载该存储的主机数量             |
| vm_num         | 使用该存储的虚拟机数量           |