# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-10
说明：处理接受命令行的命令
'''

import logging


class Logger:
    def __init__(self, file="", clevel=logging.INFO, Flevel=logging.DEBUG):
        # 设置CMD日志
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S')
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(fmt)
        self.sh.setLevel(clevel)

        # 设置文件日志
        if len(file) != 0:
            open(file, 'w', encoding='utf-8').close()
            # 设置日志文件路径/格式/日志级别
            self.logger = logging.getLogger(file)
            self.logger.setLevel(logging.DEBUG)
            self.fh = logging.FileHandler(file, encoding='utf-8')
            self.fh.setFormatter(fmt)
            self.fh.setLevel(Flevel)
            self.logger.addHandler(self.fh)

        self.logger = logging.root.addHandler(self.sh)
        self.logger.addHandler(self.sh)

    def debug(self, message):
        self.logger.debug(message)
        self.close()

    def info(self, message):
        self.logger.info(message)
        self.close()

    def war(self, message):
        self.logger.warning(message)
        self.close()

    def error(self, message):
        self.logger.error(message)
        self.close()

    def cri(self, message):
        self.logger.critical(message)
        self.close()

    def close(self):
        try:
            self.sh.close()
            self.fh.close()
        except:
            pass


def get_logger(file="", clevel=logging.INFO, Flevel=logging.DEBUG):
    def gene_method():
        logger = Logger(file=file, clevel=clevel, Flevel=Flevel)
        return logger

    return gene_method


if __name__ == "__main__":
    file="./log.log"
    a = get_logger(file=file)()
    print(a.logger.debug("12322"))
