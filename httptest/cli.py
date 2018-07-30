# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-10
说明：处理接受命令行的命令
'''
import sys, argparse
from httptest import client
from httptest.logger import Logger


LOG_FILE = "./test.log"


def main():
    parser = argparse.ArgumentParser()
    # 版本号
    parser.add_argument(
        '-v', '--version', action='store_true',
        help="Show the HttpTest version")

    # 测试路径
    parser.add_argument(
        '-t', '--test_path', nargs='*',
        help="Set the test_set file path")

    # 测试日志
    parser.add_argument(
        '-l', '--logger', action='store_true',
        help="Set the log status")

    args = parser.parse_args()

    # 版本号
    if args.version:
        print("HttpTest v1.0\n(c) 2017-2018 HttpTest Team. All Rights Reserved.")
        exit(0)

    # 初始化日志
    if args.logger:
        Logger(log_file=LOG_FILE)

    # todo 测试路径需要跟run入口对接
    if args.test_path:
        print(args.test_path)
        client.HttpTester().run()


# if __name__ == "__main__":
#     main()