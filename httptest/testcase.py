# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：解析json为用例的各种方法
'''
import json
from httptest.logger import Logger
from httptest import exception
logger = Logger()


def _validate_some_items(items):
    """
    根据内容的值和类型进行校验
    :param items:
        [
            (value, type, True),
            (someone, dict),
            (sometwo, str)
        ]
        allow_none:是否允许值为空
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


# todo 等最终的格确定了做这里
def _basic_format_validate(case):
    """
    :校验标准测试用例格式
        标准格式如下:
        {
                "request": "{"url": "http://127.0.0.1:2333/test", "json": {"aaa": "bbb"}, "method": "POST", "headers": {"Content-Type": "application/json"}, "timeout": 10}",
                "testname": "用例99",
                "testtype": "testcass",
                "validate": "[{"Equal": ["r.json()","request["json"]"]},{"Equal": ["r.status_code","200"]}]"
        }
    :param case:
            校验格式
             request:
             1.request不能为空;url不能为空
             2.method不能为空:get/post；
             3.header不能为空，只能为json；
             4.json不能为空；
             5.timeout不能只能为数字，大于0

             testname:
             1.不能为空

             testtype:
             1.不能为空
             2.testcass和testsuite

             validate：
             1.不能为空
    :return: False失败,True成功

     """
    if not isinstance(case, dict):
        try:
            case = json.loads(case, encoding="utf-8")
        except Exception as e:
            return False

    # request
    try:
        request = json.loads(case["request"], encoding="utf-8")
        # request
        if request is None or \
                not isinstance(request, dict) or request == {}:
            return False

        # url
        if request["url"] is None or \
                not isinstance(request["url"], str) or request["url"] == "":
            return False

        # method
        if request["method"] is None or \
                not isinstance(request["method"], str):
            return False
        if request["method"] not in ("get", "post", "GET", "POST"):
            return False

        # timeout
        if request["timeout"] is None or \
                not isinstance(request["timeout"], int) or request["timeout"] == "":
            return False

        # json
        if request["json"] is None or \
                not isinstance(request["json"], dict) or request["json"] == {}:
            return False

        # headers
        if request["headers"] is None or \
                not isinstance(request["headers"], dict) or request["headers"] == {}:
            return False
        if "Content-Type" not in request["headers"].keys() \
                and "application/json" not in request["headers"].values():
            return False
    except (Exception, KeyError, SyntaxError) as e:
        return False

    # testname
    try:
        testname = case["testname"]
        if testname is None or \
                not isinstance(testname, str) or testname == "":
            return False
    except (Exception, KeyError, SyntaxError) as e:
        return False

    # testtype
    try:
        testtype = case["testtype"]
        if testtype is None or \
                not isinstance(testtype, str) or testtype == "":
            return False
        if testtype not in ("testcass", "testsuite"):
            return False
    except (Exception, KeyError, SyntaxError) as e:
        return False

    # validate
    # todo validate str to dict异常，需要解决这个问题！！
    try:
        validate = case["validate"]
        if validate is None or \
                not isinstance(validate, str) or validate == "":
            return False

    except (Exception, KeyError, SyntaxError) as e:
        return False

    return True




def validate_json_case(filename):
    """
    检查json文件的内容
    {
        "testcase": {
            "name": "teatname",
            "request": {
                "url": "http://127.0.0.1/test",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "username": "admin",
                    "password":"123456"
                }
            },
            "extract": [
                {"token": "$token"}
                ],
            "validate": [
                {"eq": ["status_code", 200]}
                ]
            }
    }
    """
    try:
        # 读取json文件
        with open(filename, 'r') as f:
            json_obj = json.load(f)

        # 校验testcase/extract/validate是否存在
        # extract = json_obj["extract"]
        testcase = json_obj["testcase"]
        # validate = json_obj["validate"]

        # 校验testcase/name;testcase/name;
        testcase_name = testcase["name"]
        testcase_request = testcase["request"]
        testcase_request_url = testcase_request["url"]
        testcase_request_json = testcase_request["json"]
        testcase_request_method = testcase_request["method"]

        # 校验testcase/request/headers/content-type的各级内容
        testcase_request_headers = testcase_request["headers"]
        testcase_request_headers_content = testcase_request_headers["Content-Type"]

        # 添加所有需要校验的items
        valids = []
        valids.append((testcase_name, str))
        valids.append((testcase_request, dict))
        valids.append((testcase_request_url, str))
        valids.append((testcase_request_method, str))
        valids.append((testcase_request_headers, dict))
        valids.append((testcase_request_headers_content, str))

        # json允许为空
        valids.append((testcase_request_json, dict, True))

        # 校验失败，跑出异常由try捕获统一处理
        if not _validate_some_items(valids):
            raise Exception

    except (Exception, exception.NotFoundCaseError):
        raise exception.NotFoundCaseError("用例格式错误,请检查测试用例格式")

    return json_obj


if __name__ == "__main__":
    file = "../test_json1.json"
    print(validate_json_case(file))
