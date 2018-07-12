# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-10
说明：日志工具
'''

import logging
from functools import wraps


LOG_LEVEL = {
    "info":     logging.INFO,
    "debug":    logging.DEBUG,
    "error":    logging.ERROR,
    "warning":  logging.WARNING,
    "critical": logging.CRITICAL
}


# 单例模式解决多线程和配置问题
def _singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


"""
只需要初始化一次就行了
"""
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
            file_handler.setLevel(LOG_LEVEL[log_level.lower()])     # 设置日志级别
            file_handler.setFormatter(fmt)  # 设置格式
            self.logger.addHandler(file_handler)    # 添加handle

        # 终端handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL[log_level.lower()])
        console_handler.setFormatter(fmt)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    Logger("").info("222")
    Logger().debug("222222")
    Logger("./log.log").info("123")

