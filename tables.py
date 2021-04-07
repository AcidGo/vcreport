from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VCReport(Base):
    __tablename__ = "vcreport"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    create_time = Column(DateTime, nullable=False, comment="创建批次时间")
    alias = Column(String(100), nullable=False, comment="vCenter 人为设定别名")
    name = Column(String(100), nullable=False, comment="vCenter 系统内命名")
    flag = Column(String(100), nullable=False, comment="vSphere 标记")
    cluster_total = Column(Integer, nullable=False, comment="管理集群数量")
    host_total = Column(Integer, nullable=False, comment="管理接入的 ESXi 主机数量")
    host_running_total = Column(Integer, nullable=False, comment="正在运行的主机数量")
    vm_total = Column(Integer, nullable=False, comment="虚拟机的总数量")
    vm_running_total = Column(Integer, nullable=False, comment="正在运行的虚拟机的数量")
    ds_total = Column(Integer, nullable=False, comment="存储的总数量")
    ds_share_total = Column(Integer, nullable=False, comment="共享存储的总数量")

class DSReport(Base):
    __tablename__ = "dsreport"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    create_time = Column(DateTime, nullable=False, comment="创建批次时间")
    name = Column(String(100), nullable=False, comment="存储名称")
    vc_name = Column(String(100), comment="存储所在 vCenter 的名称")
    fs_type = Column(String(20), nullable=False, comment="存储所在 vCenter 的名称")
    space_total = Column(BigInteger, nullable=False, comment="存储的总容量")
    space_used = Column(BigInteger, nullable=False, comment="存储的已用容量")
    space_free = Column(BigInteger, nullable=False, comment="存储的可用容量")
    host_num = Column(Integer, nullable=False, comment="挂载该存储的主机数量")
    vm_num = Column(Integer, nullable=False, comment="使用该存储的虚拟机数量")