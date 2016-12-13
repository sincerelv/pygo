import MySQLdb
import datetime


class DAO():
    def getconn(self):
        """"""
        self.__conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='BigJoey',
            db='ygo',
        )
        self.__cur = self.__conn.cursor()

    def insert(self):
        """"""
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "insert into openCodeList values(%s,%s,%s)"
        self.__cur.execute(sql1, (object["expect"], object["openCode"], dt))
        self.__cur.close()
        self.__conn.commit()
        self.__conn.close()

    def update(self):
        """"""
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "update openCodeList set values(%s,%s,%s)"
        self.__cur.execute(sql1, (object["expect"], object["openCode"], dt))
        self.__cur.close()
        self.__conn.commit()
        self.__conn.close()
