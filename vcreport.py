
from config import *
from collecter import VCWorker
from reporter import DBReport

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
    init_logger("debug")
    try:
        report_create_time = datetime.datetime.now()
        dbr = DBReport()
        dbr.login(REPORT_DB_DSN)

        for vc, vc_login_args in VC_CONFIG_MAP.items()
            logging.info(f"starting deal with vc: {vc}")
            vcc = VCWorker()
            try:
                vcc.login(vc_login_args)
                pdata = vcc.collect(
                    v_obj_type = VC_BIND_VIEW_OBJ_TYPE,
                    p_obj_type = VC_BIND_PROP_OBJ_TYPE,
                    path_set = VC_BIND_PROP_PATH_SET,
                )
                # TODO(20210407): add prop selecting and insert it to db
                logging.info(pdata)
            except Exception as e:
                logging.error(f"get an err when deal with {vc}: {str(e)}")
                logging.exception(e)
            finally:
                vcc.logout()

    except Exception as e:
        logging.exception(e)
        exti(1)

