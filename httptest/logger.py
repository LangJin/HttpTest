# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-10
说明：日志工具
'''
import ctypes
import logging
from functools import wraps


LOG_LEVEL = {
    "info":     logging.INFO,
    "debug":    logging.DEBUG,
    "error":    logging.ERROR,
    "war":      logging.WARNING,
    "cri":      logging.CRITICAL,
}

LOG_COLOR = {
    "red":      0x04,
    "white":    0x0007,
    "yellow":   0x04 | 0x02,
}


# 设置控制台颜色
def set_color(color, handle=ctypes.windll.kernel32.GetStdHandle(-11)):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool


# 单例模式解决多线程和配置问题
def _singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


# 在cli中初始化一次就行了
@_singleton
class Logger:
    def __init__(self, log_file=None, log_level="info"):
        """
        初始化logger信息
        :param log_file: 日志文件路径
        :param log_level: info/debug/error/warning/critical
        :return:
        """
        self.logger = logging.root
        self.logger.setLevel(LOG_LEVEL[log_level.lower()])

        # 日志文件
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S')
        if log_file:
            file_handler = logging.FileHandler(filename=log_file, mode='a+', encoding="utf-8")  # 追加文件
            file_handler.setLevel(LOG_LEVEL[log_level.lower()])                                 # 设置日志级别
            file_handler.setFormatter(fmt)                                                      # 设置格式
            self.logger.addHandler(file_handler)                                                # 添加handle

        # 终端handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL[log_level.lower()])
        console_handler.setFormatter(fmt)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        set_color(LOG_COLOR["yellow"])
        self.logger.warning(message)
        set_color(LOG_COLOR["white"])

    def error(self, message):
        set_color(LOG_COLOR["red"])
        self.logger.error(message)
        set_color(LOG_COLOR["yellow"])

    def cri(self, message):
        set_color(LOG_COLOR["red"])
        self.logger.critical(message)
        set_color(LOG_COLOR["white"])


logger = Logger()

if __name__ == "__main__":
    logger = Logger()
    logger.info("222")
    logger.war("123")
    logger.error("123")
    logger.cri("123")

