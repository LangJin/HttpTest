# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：解析json用例中的变量
'''


def get_global_values(request):
    '''
    替换request里带了$的参数为全局变量中的值。
    {
        "url": "http://127.0.0.1:2333/test",
        "json": {'token': '$token'},
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "timeout": 10
    }
    '''
    pass


def extract_global_values(extract):
    '''
    [
        {"token":"r.json()["data"]"},
        {"token":"r.json()["data"]"}
    ]
    '''
    execlist = []
    for extdict in extract:
        key = list(extdict.keys())[0]
        value = extdict[key]
        extfuc = "extracts['%s'] = %s" % (key, value)
        execlist.append(extfuc)
    return execlist


def run_execs_test(execlist):
    '''
    执行赋值类型的表达式
    extracts['token'] = 'ssdsfsdf4s6f54s6f1a3s'
    '''
    # print(**arg)
    if len(execlist) != 0:
        for execkey in execlist:
            print(execkey)
            exec(execkey)
