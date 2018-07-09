# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：启动接口测试的入口
'''
import unittest
from httpcore import httptest
from respones import resobj
from testcase import import_json_file, chick_type_json
from validate import chick_validate
from logger import Logger

logger = Logger()


class TestCass(unittest.TestCase):

    def runTest(self):
        '''
        ?
        '''
        filename = "test_json.json"
        filename = import_json_file(filename)
        json_context = chick_type_json(filename)
        request = json_context.get("request")
        validates = json_context.get("validates")
        response = httptest(request)
        validatelist = resobj(response, validates)
        chick_validate(validatelist)


suite = unittest.TestSuite()
suite.addTest(TestCass())

runner = unittest.TextTestRunner()
runner.run(suite)