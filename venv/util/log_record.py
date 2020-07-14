import logging
import os,time
import logging.config
from util.read_ini import ReadIni

def get_filename(case_name = "case_log"):
    dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\logs\\" + time.strftime("%Y-%m-%d") + "\\")
    isExists = os.path.exists(dirname)
    # 判断结果
    if not isExists:
        os.makedirs(dirname)
    filename = os.path.join(dirname + case_name + "  " + time.strftime("%H_%M_%S") + ".log")
    ReadIni().write_data("log_file",filename,"log")

def get_logger(name="fileLogger"):
    #首先判断logs目录是否存在，不存在则创建
    dirs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\logs")
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    log_name = ReadIni().get_value("log_file","log")

    log_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config/log.conf")
    logging.config.fileConfig(log_conf,log_name)
    logger=logging.getLogger(name)
    return logger



if __name__ == "__main__":
    print(get_filename())
    logger = get_logger("../logs/test.log")
    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
