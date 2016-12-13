# encoding: UTF-8
import json
import random
import urllib
import urlparse
import math
import numpy as np
import time

import pandas as pd
import requests
import prl


def isBig(num):
    """"""
    return int(num) >= 5


def isEven(num):
    """"""
    return int(num) % 2 == 0


def toBig(code):
    """"""
    list = []
    for x in code.split(','):
        list.append(isBig(x) and 'b' or 's')
    return list


def toEven(code):
    """"""
    list = []
    for x in code.split(','):
        list.append(isEven(x) and 'e' or 'o')
    return list


def numCount(code):
    codes = code.split(',')
    list = []
    for n in range(10):
        """"""
        list.append(codes.count(str(n)))
    return list


def twice(code1, code2, cat):
    """"""
    list = []
    list1 = toBig(code1)
    list2 = toBig(code2)
    if cat == 'e':
        list1 = toEven(code1)
        list2 = toEven(code2)

    for i in range(len(list1)):
        """"""
        list.append(list1[i] == list2[i] and 't' or list2[i])
    return list


def third(code1, code2, code3, cat):
    """"""
    result = []
    list1 = twice(code1, code2, cat)
    list2 = twice(code2, code3, cat)

    for i in range(len(list1)):
        """"""
        if list1[i] == 't' and list2[i] != 't':
            result.append(bytes(i) + '_' + list2[i])
            # else:
            #     list.append(False)
    return result


def anHis(openCode, num, cat):
    count = 0
    for o in openCode:
        if cat == 'e' or cat == 'o':
            if isEven(int(o["openCode"].split(',')[num])):
                count += 1
        elif cat == 'b' or cat == 's':
            if isBig(int(o["openCode"].split(',')[num])):
                count += 1
    return len(openCode) / 2 >= count


def selectSite():
    cost = 1000
    host = ''
    hosts = ['cluba11', 'clubb66', 'clubc88', 'game11', 'game86']
    for h in hosts:
        cur = h + '.yignew.com:8077'
        conn_time = 0
        for i in range(5):
            try:
                prl.time_conn(cur)
            except requests.RequestException as e:
                print '', e.message
            else:
                conn_time += prl.time_conn(cur)

        print h, 'conn_time', conn_time
        if conn_time <= cost:
            cost = conn_time
            host = cur
    return host


def anCount(openCodeList):
    ''''''
    # for item in openCodeList:
    #     A.append(str(item['openCode']).split(',')[0])
    #     B.append(str(item['openCode']).split(',')[1])
    #     C.append(str(item['openCode']).split(',')[2])
    #     D.append(str(item['openCode']).split(',')[3])
    #     E.append(str(item['openCode']).split(',')[4])
    #     # openCode.append(code['openCode'])
    #     expect.append(item['expect'])
    #
    # print A
    # print expect
    # ts = pd.Series(E, index=expect)
    # print ts.cumsum
    # print openCode
    # for code in openCode:
    #     print code

    # for i in range(10):
    #     print all.count(i)


if __name__ == '__main__':
    ''''''
    r = None
    print type(r)
    if r:
        print 'ww'
    # list = ['3', '2']
    # if len(list):
    #     print '1', '中'
    # anCount("{'expect': '201612010991', 'openCode': '3,7,0,9,1'}")
    # print selectSite()
    # print prl.time_conn('cluba11.yignew.com:8077')
    # print prl.time_conn('clubb66.yignew.com:8077')
    # print prl.time_conn('clubc88.yignew.com:8077')
    # print prl.time_conn('game11.yignew.com:8077')
    # print prl.time_conn('game86.yignew.com:8077')
    # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print 2 <= 1 <= 2

    # print pd.date_range('1/1/2000', periods=1000)
    # print pd.DataFrame(np.random.randn(1000, 4))
    # print toBig('2,3,6,4,9')
    # cound = []
    # code1 = '2,3,6,4,9'
    # code2 = '2,5,3,4,6'
    # code3 = '6,3,6,4,3'
    # list = third(code1, code2, code3, 'b')
    # for i in range(10):
    #     if i % 3:
    #         print i
    # ''''''
    #     if list[i]:
    #         ''''''
    #         cound.append(i)
    #
    # print cound
    # if isBig(cound[random.randint(0, len(cound) - 1)]):
    #     ''''''
    # if isBig(code3.split(',')[i]):
    #     ''''''
    #
    # else:
    #     ''''''
    #
    # print isBig(6)
    # print twice('2,3,6,4,9', '2,5,3,4,6', 'e')
    # print third('2,3,1,4,9', '2,5,3,4,6', '6,3,6,4,3', 'e')
    # print numCount('2,3,6,5,9,2,6,9,5,6,4,9,2,3,6,5,3,6,4,2,3,6,4,3,4,2,3,4,3,6,4,2,3,6,4,1,0,7,8')
