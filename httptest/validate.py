# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：对预期结果和实际结果做校验
'''

from httptest.exception import ValidateError

def chick_validate(validatelist):
    '''
    validatelist = ["a=1","b=2"]
    '''
    for validate in validatelist:
        print(validate)
        if eval(validate):
            print("测试通过")
        else:
            raise ValidateError(validate,"预期结果与实际结果不一致！")