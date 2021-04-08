import datetime
import logging

from config import *
from collecter import VCWorker
from reporter import DBReport
from tables import DSReport, VCReport

def init_logger(level, logfile=None):
    """日志功能初始化。
    如果使用日志文件记录，那么则默认使用 RotatingFileHandler 的大小轮询方式，
    默认每个最大 10 MB，最多保留 5 个。
    Args:
        level: 设定的最低日志级别。
        logfile: 设置日志文件路径，如果不设置则表示将日志输出于标准输出。
    """
    import os
    import sys
    from logging.handlers import RotatingFileHandler
    if not logfile:
        logging.basicConfig(
            level = getattr(logging, level.upper()),
            format = "%(asctime)s [%(levelname)s] %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )
    else:
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, level.upper()))
        if logfile.lower() == "local":
            logfile = os.path.join(sys.path[0], os.path.basename(os.path.splitext(__file__)[0]) + ".log")
        handler = RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=5)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logging.info("Logger init finished.")

if __name__ == "__main__":
    init_logger("info", "local")
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    try:
        report_create_time = datetime.datetime.now()
        dbr = DBReport()
        dbr.login(REPORT_DB_DSN)

        for vc, vc_login_args in VC_CONFIG_MAP.items():
            logging.info(f"starting deal with vc: {vc}")
            vcc = VCWorker()
            ds_url_set = set()
            try:
                vcreport_row = VCReport(
                    create_time = report_create_time,
                    alias = vc,
                    name = vc,
                    cluster_total = 0,
                    host_total = 0,
                    host_running_total = 0,
                    cpu_total = 0,
                    mem_total = 0,
                    vm_total = 0,
                    vm_poweredoff_total = 0,
                    ds_total = 0,
                    ds_share_total = 0,
                )

                # login vCenter session
                vcc.login(**vc_login_args)

                # for VCReport
                # 1. coll cluster
                pdata = vcc.collect(
                    v_obj_type = [vim.ClusterComputeResource],
                    p_obj_type = vim.ClusterComputeResource,
                    path_set = ["name"],
                )
                vcreport_row.cluster_total = len(pdata)

                # 2. coll host
                pdata = vcc.collect(
                    v_obj_type = [vim.HostSystem],
                    p_obj_type = vim.HostSystem,
                    path_set = [
                        "name", 
                        "runtime",
                        "summary.hardware",
                        "vm",
                        "datastore",
                    ],
                )
                for pset in pdata:
                    for p in pset.propSet:
                        if p.name == "name":
                            vcreport_row.host_total += 1
                        if p.name == "runtime" and p.val.connectionState == "connected" and p.val.powerState == "poweredOn":
                            vcreport_row.host_running_total += 1
                        if p.name == "summary.hardware":
                            vcreport_row.mem_total += p.val.memorySize
                            vcreport_row.cpu_total += p.val.numCpuCores
                        if p.name == "vm":
                            for vm in p.val:
                                if vm.config.template is False:
                                    vcreport_row.vm_total += 1
                                if vm.runtime.powerState != vim.VirtualMachine.PowerState.poweredOn:
                                    vcreport_row.vm_poweredoff_total += 1
                        if p.name == "datastore":
                            for ds in p.val:
                                if ds.info.url in ds_url_set:
                                    continue
                                vcreport_row.ds_total += 1
                                if ds.summary.multipleHostAccess is True:
                                    vcreport_row.ds_share_total += 1
                                ds_url_set.add(ds.info.url)

                # fuck pymysql
                vcreport_row.cpu_total = str(vcreport_row.cpu_total)
                vcreport_row.mem_total = str(vcreport_row.mem_total)
                dbr.report(vcreport_row)

                # for DSReport
                pdata = vcc.collect(
                    v_obj_type = [vim.Datastore],
                    p_obj_type = vim.Datastore,
                    path_set = [
                        "name",
                        "summary",
                        "host",
                        "vm",
                    ]
                )
                for pset in pdata:
                    dsreport_row = DSReport(
                        create_time = report_create_time,
                        vc_alias = vc,
                        vc_name = vc,
                        space_total = 0,
                        space_free = 0,
                        space_uncommit = 0,
                    )
                    for p in pset.propSet:
                        if p.name == "name":
                            dsreport_row.name = p.val
                        if p.name == "summary":
                            dsreport_row.is_access = p.val.accessible
                            dsreport_row.is_multiple = p.val.multipleHostAccess
                            dsreport_row.fs_type = p.val.type
                            dsreport_row.space_total = p.val.capacity
                            dsreport_row.space_free = p.val.freeSpace
                            dsreport_row.space_uncommit = p.val.uncommitted if p.val.uncommitted is not None else 0
                        if p.name == "host":
                            dsreport_row.host_num = len(p.val)
                        if p.name == "vm":
                            dsreport_row.vm_num = len(p.val)
                    # fuck pymysql
                    dsreport_row.space_total = str(dsreport_row.space_total)
                    dsreport_row.space_free = str(dsreport_row.space_free)
                    dsreport_row.space_uncommit = str(dsreport_row.space_uncommit)
                    dbr.report(dsreport_row)

            except Exception as e:
                logging.error(f"get an err when deal with {vc}: {str(e)}")
                logging.exception(e)
            finally:
                vcc.logout()

    except Exception as e:
        logging.exception(e)
        exit(1)
