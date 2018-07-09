# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：对接口的响应的数据进行处理
'''

def getassert(key):
    asserts = {
        "Equal": "==",
        "NotEqual": "!=",
        "True": "is True",
        "False": "is False",
        "Is": "is",
        "IsNot": "is not",
        "IsNone": "is None",
        "IsNotNone": "is not None",
        "In": "in",
        "NotIn": "not in",
        "IsInstance": "isinstance",
        "NotIsInstance": "not isinstance"
    }
    value = asserts[key]
    # print(value)
    return value

def resobj(response, validates):
    '''
    "validates": {
        "Equal": ["resdata['status']", 200],
        "Equal": ["status_code", 200]
        }
    '''
    resdata = {}
    try:
        resdata["body"] = response.json()
    except:
        resdata["body"] = response.text
    resdata["status"] = response.status_code
    validatelist = []
    for key, value in validates.items():
        first = eval(value[0])
        second = eval(value[1])
        assertvalue = getassert(key)
        validate = str(first) + assertvalue + str(second)
        validatelist.append(validate)
    return validatelist