# coding: UTF-8
import datetime
import traceback

import MySQLdb
import requests
import time
import os
import sys
import random
import re
from pytesser import *

from unit import *


class ZhiHuClient(object):
    """连接知乎的工具类，维护一个Session
    2016.11.11

    用法：

    client = ZhiHuClient()

    # 第一次使用时需要调用此方法登录一次，生成cookie文件
    # 以后可以跳过这一步
    client.login("username", "password")

    # 用这个session进行其他网络操作，详见requests库
    session = client.getSession()
    """

    # 网址参数是账号类型
    Host = "game86.yignew.com:8077"
    TYPE_EMAIL = "email"
    homeURL = r"http://" + Host
    loginURL = homeURL + "/ct-data/acegi/j_acegi_security_check"
    captchaURL = homeURL + "/ct-data/acegi/captcha?" + str(time.time())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": Host,
        "Upgrade-Insecure-Requests": "1",
    }
    captchaFile = os.path.join(sys.path[0], "captcha.png")

    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='BigJoey',
        db='ygo',
    )
    cur = conn.cursor()

    cumuli = -1
    multi = [1, 3, 8, 24, 72, 180, 450, 1100, 3000, 8000, 24000]
    tasks = {'lastExpect': 0, 'curExpect': 0, 'curType': 1, 'multi': multi[0], 'num': 0, 'code': '0', 'foll': True}
    codes = {'s': '0,1,2,3,4', 'b': '5,6,7,8,9', 'e': '0,2,4,6,8', 'o': '1,3,5,7,9'}

    def __init__(self):
        os.chdir(sys.path[0])  # 设置脚本所在目录为当前工作目录
        self.__session = requests.Session()
        self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
        self.setHost()

    def setHost(self):
        self.Host = selectSite()
        self.homeURL = r"http://" + self.Host
        self.loginURL = self.homeURL + "/ct-data/acegi/j_acegi_security_check"
        self.captchaURL = self.homeURL + "/ct-data/acegi/captcha?" + str(time.time())

    def openCode(self, shortName):
        try:
            r = self.__session.post(self.homeURL + '/ct-data/openCodeList?shortName=' + shortName + '&num=5&Rand=' + str(time.time()))
        except requests.RequestException as e:
            print e.message
            return self.openCode(shortName)
        else:
            print 'r.json()', r.json()
            if r.json()["sign"]:
                result = r.json()["openCodeList"][0]
                # print 'result ', result
                if result["expect"] == self.tasks['curExpect']:
                    time.sleep(5)
                    return self.openCode(shortName)
                return r
            else:
                return

    # 登录
    def login(self, username, password):
        """"""
        self.__username = username
        self.__password = password
        self.__loginURL = self.loginURL
        # 下载验证码图片
        while True:
            captcha = self.open(self.captchaURL)
            if captcha and captcha is not 'NoneType':
                captcha = captcha.content
                with open(self.captchaFile, "wb") as output:
                    output.write(captcha)
                    # 人眼识别
                print("=" * 50)
                # print("已打开验证码图片，请识别！")
                # subprocess.call(self.captchaFile, shell=True)
                time.sleep(3)
                captcha = re.match(r"\w+", image_file_to_string('captcha.png'))
                if captcha and type(captcha) is not 'NoneType':
                    # print captcha.group(0)
                    captcha = captcha.group(0).replace('_', '')
                    if len(captcha) == 4 and captcha.isalnum():
                        """"""
                        # os.remove(self.captchaFile)
                        # 发送POST请求
                        data = {
                            "ua": "web",
                            "j_password": self.__password,
                            'j_username': self.__username,
                            "validateCode": captcha
                        }
                        # print data
                        res = self.__session.post(self.__loginURL, data=data)
                        # print("=" * 50)
                        # print(self.__session.headers)  # 输出脚本信息，调试用
                        if res.json()["sign"]:
                            print("登录成功")
                            break
                        else:
                            print("登录失败")
                            print res.json()["message"]

    def first(self, shortName):
        session = self.__session

        r = session.post(self.homeURL + '/ct-data/openCodeList?shortName=' + shortName + '&num=200&Rand=' + str(time.time()))
        # anCount(r.json()["openCodeList"])
        result = r.json()["openCodeList"][0]
        self.tasks['lastExpect'] = result["expect"]

        # 一次插入多条记录
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for o in r.json()["openCodeList"]:
            sql = "insert into openCodeList values(%s,%s,%s)"
            self.cur.execute(sql, (o["expect"], o["openCode"], dt))

        self.conn.commit()

    def doFoll(self, isFoll):
        if isFoll:
            if self.tasks['curType'] == 's':
                ''''''
                self.tasks['curType'] = 'b'
                self.tasks['code'] = self.codes['b']
            elif self.tasks['curType'] == 'b':
                ''''''
                self.tasks['curType'] = 's'
                self.tasks['code'] = self.codes['s']
                # continue
                ''''''
            elif self.tasks['curType'] == 'o':
                ''''''
                self.tasks['curType'] = 'e'
                self.tasks['code'] = self.codes['e']
            elif self.tasks['curType'] == 'e':
                ''''''
                self.tasks['curType'] = 'o'
                self.tasks['code'] = self.codes['o']

    def open(self, url, delay=0, timeout=10):
        """打开网页，返回Response对象"""
        if delay:
            time.sleep(delay)

        try:
            self.__session.get(url, timeout=timeout)
        except requests.RequestException as e:
            print e
            print traceback.print_exc()
        else:
            ''''''
            return self.__session.get(url, timeout=timeout)
            # finally:
            #     ''''''
            # return self.__session.get(url, timeout=timeout)

    def plot(self, openCodeList):

        result = openCodeList[0]
        print result
        print '=' * 100
        print u'result', result
        print 'openCode', str(result["openCode"].split(',')[self.tasks['num']])
        print 'tasks 202 ', self.tasks
        if result["expect"] == self.tasks['lastExpect']:
            r1 = openCodeList[1]["openCode"]
            r2 = openCodeList[2]["openCode"]
            # print r2
            # print r1
            # print result
            list = third(r2, r1, result["openCode"], 'b') + third(r2, r1, result["openCode"], 'e')
            print '=' * 100
            sql1 = "insert into openCodeList values(%s,%s,%s)"
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cur.execute(sql1, (result["expect"], result["openCode"], dt))
            self.conn.commit()
            print 'list', list
            if str(result["openCode"].split(',')[self.tasks['num']]) in str(self.tasks['code']) or self.tasks['curType'] <= 1:
                ''''''
                if self.tasks['curType'] != 0:
                    print 'get'
                    self.cur.execute('update task set result = %s where expect=%s;', ['get', result["expect"]])
                    self.conn.commit()

                self.cumuli = 0
                # print 'num', num

                if len(list):
                    num = random.randint(0, len(list) - 1)
                    print 'list[num][2] ', list[num][2]
                    # print 'anHis', anHis(r.json()["openCodeList"], int(list[num][0]), list[num][2])
                    self.tasks['foll'] = anHis(openCodeList, int(list[num][0]), list[num][2])
                    # print 'list', list[num], num
                    # print ' list[num][3] ', list[num][2]
                    # print 'result', result["openCode"].split(','), result["openCode"].split(',')[int(list[num][0])]
                    self.tasks['multi'] = self.multi[self.cumuli]
                    self.tasks['num'] = int(list[num][0])
                    self.tasks['curType'] = list[num][2]
                    self.tasks['code'] = self.codes[list[num][2]]
                else:
                    self.tasks['curType'] = 0
            else:
                if self.tasks['curType'] != 0:
                    self.cumuli += 1
                    if self.cumuli >= len(self.multi):
                        self.cumuli = 0

                    if self.multi[self.cumuli] % 3 == 0:
                        if len(list) >= 3:
                            # if self.tasks['code'] != '0':
                            num = random.randint(0, len(list) - 1)
                            self.tasks['num'] = int(list[num][0])
                            self.tasks['curType'] = list[num][2]
                            # print 'not get  ', cumuli
                            # print ' tasks code ', self.tasks['code']
                            # print ' tasks curType ', self.tasks['curType']
                            # print ' tasks foll ', self.tasks['foll']
                    self.tasks['multi'] = self.multi[self.cumuli]
                    self.doFoll(self.tasks['foll'])

            if self.cumuli >= 7:
                output = open('data.txt', 'a')
                output.write('over ' + str(self.tasks['multi']) + ' ;' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' \n')

            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql1 = "insert into task values(%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql1,
                             (self.tasks['curExpect'], self.tasks['code'], self.tasks['num'], self.tasks['multi'], self.tasks['curType'], '', dt))
            self.conn.commit()
        pass

    def start(self):
        """"""
        shortName = 'ffc'
        # 用这个session进行其他网络操作，详见requests库
        try:
            self.login("6sincerev", "BigJoey*6")
            self.first(shortName)
        except:
            return

        while True:
            try:
                r = self.__session.post(self.homeURL + '/ct-data/loadOpenTime?shortName=' + shortName + '&Rand=' + str(random.random()))
                # print r.json()
                time.sleep(r.json()['remainTime'])
                self.tasks['curExpect'] = r.json()['currFullExpect']
                self.tasks['lastExpect'] = r.json()['lastFullExpect']
                # r = self.openCode(shortName)
                # print r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常

                # r = self.openCode(shortName)
                # result = r.json()["openCodeList"][0]
                # result = r.json()["openCodeList"][0]
                # if result["expect"] == self.tasks['lastExpect']:
                r = self.openCode(shortName)


            except requests.RequestException as e:
                print 'RequestException', e
                print traceback.print_exc()
                return
            else:
                ''''''
                if r:
                    self.plot(r.json()["openCodeList"])

                # finally:
                #     if conn != None:


if __name__ == '__main__':

    while True:
        client = ZhiHuClient()
        client.start()
    # print toBig('2,3,6,4,9')
    # print toEven('2,3,6,4,9')
    # print numCount('2,3,6,5,9,2,6,9,5,6,4,9,2,3,6,5,3,6,4,2,3,6,4,3,4,2,3,4,,3,6,4,2,3,6,4,1,0,7,8')

    # print third('3,5,2,4,8', '3,5,2,4,8', '6,1,7,9,2', 'e')
