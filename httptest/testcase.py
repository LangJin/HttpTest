# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-16
说明：解析json为用例的各种方法
'''
import json
import exception
from logger import logger


def _validate_some_items(items):
    """
    根据内容的值和类型进行校验
    :param items:
        [
            (value, type, True),
            (someone, dict),
            (sometwo, str)
        ]
    :return: False:校验失败；True:校验成功
    """
    for item in items:
        k, v = item[0], item[1],
        # 获取需要校验值的类型和是否为空项目，如果出现异常，则默认为可以为空
        try:
           allow_none = item[2]
        except:
            allow_none = False # 默认不为空

        # 首先判断是否可以为空，再进行校验
        if allow_none is False:
            if len(k) == 0 or not isinstance(k, v): # 这里用len来做空值判断，可以兼容各种数据类型
                return False
        else:
            if not isinstance(k, v):
                return False

    return True


def import_json_file(filename):
    '''
    filename = "test_*.json"
    说明：判断导入的json文件名/格式是否合法
    '''
    filetype = filename.split(".")
    if filetype[-1] == "json" and filename.startswith("test"):
        return filename
    else:
        logger.error("{}导入的JSON文件格式不正确，请检查JSON格式！".format(filename))
        exit()


def validate_json_case(filename):
    """
    说明：校验json文件格式
    :param filename : json文件的路径
    :return True: 校验通过; Flase: 校验失败
    """
    valid_items = []
    try:
        # 读取json文件并生成json对象
        with open(filename, 'r', encoding="utf-8") as f:
            json_obj = json.load(f)

        # 检查testcase项, 默认每个key是必填，如果不存在某个key时直接获取则会抛出异常
        t_request = eval(json_obj["request"])                           # testcase/request
        t_request_url = t_request["url"]                                # testcase/request/url
        t_request_json = t_request["json"]                              # testcase/request/json
        t_request_method = t_request["method"]                          # testcase/request/method
        t_request_headers = t_request["headers"]                        # testcase/request/headers
        t_request_headers_content = t_request_headers["Content-Type"]   # testcase/request/headers/content-type

        # 添加所有需要校验的items
        valid_items.append((t_request, dict))
        valid_items.append((t_request_url, str))
        valid_items.append((t_request_method, str))
        valid_items.append((t_request_headers, dict))
        valid_items.append((t_request_headers_content, str))
        valid_items.append((t_request_json, dict, True))     # 允许json内容为空

        # request各级
        if not _validate_some_items(valid_items):
            logger.error("【错误】: 测试用例的request模块校验异常，请检查该模块")
            raise Exception

        # name
        name = json_obj["name"]
        if not _validate_some_items([(name, str)]):
            logger.error("【错误】: 测试用例的name模块校验异常，请检查该模块")
            return False

        # extract
        extract = eval(json_obj["extract"])
        if not _validate_some_items([(extract, list, True)]):
            logger.error("【错误】: 测试用例的extract模块校验异常，请检查该模块")
            return False

        # validate
        validate = eval(json_obj["validate"])
        if not _validate_some_items([(validate, list, True)]):
            logger.error("【错误】: 测试用例的validate模块校验异常，请检查该模块")
            return False

    except (Exception, exception.NotFoundCaseError, exception.ValidateError) as e:
        logger.error("【错误】：校验测试用例时发生异常，测试用例校验不通过")
        return False

    return True


def har2case():
    """
    har文件转为case
    1. 获取har
    2. 提取request并转为jsoncase的request
    3. 返回
    :return:
    """

    pass


def postman2case():
    pass


if __name__ == "__main__":
    file = "../test_json.json"
    print(validate_json_case(file))