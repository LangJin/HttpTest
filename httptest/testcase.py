# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：解析json为用例的各种方法
'''
import json
from logger import Logger
import exception
logger = Logger()


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


def chick_type_json(filename):
    '''
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
    '''
    with open(filename, 'r') as f:
        json_context = json.load(f)
        # print(json_context)
    if not isinstance(json_context, dict):
        raise exception.NotFoundCaseError("用例格式错误，json数据不是list")
    if len(json_context) == 0:
        raise exception.NotFoundCaseError("在json文件中没有找到testcase")
    return json_context

