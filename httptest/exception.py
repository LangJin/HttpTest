# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：异常处理模块
'''


class Error(BaseException):
    pass

class NotFoundCaseError(Error):
    pass

class NotFoundMethodError(Error):
    pass

class ValidateError(Error):
    pass