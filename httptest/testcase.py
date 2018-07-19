# -*- coding:utf-8 -*-
'''
作者：SNake
时间：2018-7-16
说明：解析json为用例的各种方法
'''
import io
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


def _get_json_str(file_name):
    """
    打开文件重构方法
    :param file_name:
    :return:
    """
    with io.open(file_name, 'r', encoding="utf-8") as f:
        json_str = json.load(f)

    return json_str



def import_json_file(filename):
    """
    说明：判断导入的json文件名/格式是否合法
    :param filename: "test_*.json"
    :return: filename
    """
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


def har2case(filename):
    """
    har文件转为case
    :param filename:
    :return:
    """
    test_cases = []
    har_items = _get_json_str(filename)                 # 解析文件

    # 一个har可能会有多个请求
    for entry in har_items["log"]["entries"]:
        case, req = {}, {}
        case["name"] = ""                               # case/name
        case["extract"], case["validate"] = [], []      # case/extract和case/validate默认为空

        entry = entry["request"]                        # 获取har文件中的request模块
        for k, v in entry["headers"]:
            if "Content-Type" == k:
                req["header"] = {k: v}                  # case/request/header

        try:
            req["json"] = entry["postData"]["text"]     # case/request/json
        except:
            req["json"] = {}

        req["url"] = entry["url"]                       # case/request/url
        req["method"] = entry["method"]                 # case/request/method
        case["request"] = str(req).replace("\"", "'")   # case/request
        test_cases.append(case)

    return test_cases


def postman2case(filename):
    """
    postman v2.0 脚本转为 case
    :param: filename:脚本的绝对目录
    :return: 失败:[], 成功:[{case1}，{case2}...]
    """
    test_cases = []
    postman_items = _get_json_str(filename)

    for item in postman_items["item"]:
        req, case = {}, {}
        case["name"] = item["name"]                     # case/name
        case["extract"], case["validate"] = [], []      # case/extract和case/validate默认为空

        # 获取request的值
        request = item["request"]                       # request:json中的request模块数据
        for k, v in request["header"]:                  # case/request/header
            if "Content-Type" == k:
                req["header"] = {k: v}

        try:
            req["json"] = request["body"]["raw"]        # case/request/json
        except:
            req["json"] = {}

        req["url"] = request["url"]                     # case/request/url
        req["method"] = request["method"]               # case/request/method

        case["request"] = str(req).replace("\"", "'")   # 将字符串中的" 替换为 ' ，避免格式化eval失败的问题
        test_cases.append(case)                         # 将case添加到testcases中

    return test_cases


if __name__ == "__main__":
    # file = "../test_json.json"
    # print(validate_json_case(file))

    # file = "../httptest.postman_collection.json"
    # print(postman2case(file))

    file = "../har_test.har"
    print(har2case(file))