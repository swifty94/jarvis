from visualizer import GetSQLData
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
import mysql.connector

class CreatePlot():
    def __init__(self, sql, title):
        self.sql = sql
        self.title = title

    def ParamVsTime(self):
        dbconfig = {
        'host':     '127.0.0.1',
        'user':     'root',
        'password':  'root',
        'database': 'pyguard_v1',
        }
        mydb = mysql.connector.connect(pool_name = "pyguard_v1",
                                       pool_size = 10,
                                       **dbconfig)
        cursor = mydb.cursor()
        cursor.execute(self.sql)
        result = cursor.fetchall()
        param = []
        time = []
        for item in result:
            param.append(item[0])
            time.append(item[1])
        dates = [dateutil.parser.parse(s) for s in time]
        plt.subplots_adjust(bottom=0.3, left=0.2)
        plt.xticks( rotation=50 )        
        ax=plt.gca()
        ax.set_xticks(dates)
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(param,dates)
        plt.savefig(f'static/{self.title}_plot.png')
        return plt.clf()

class CreateBar():
    def __init__(self, sql, title):
        self.sql = sql
        self.title = title
    
    def ParamVsParam(self):
        dbconfig = {
        'host':     '127.0.0.1',
        'user':     'root',
        'password':  'root',
        'database': 'pyguard_v1',
        }
        mydb = mysql.connector.connect(pool_name = "pyguard_v1",
                                       pool_size = 10,
                                       **dbconfig)
        cursor = mydb.cursor()
        cursor.execute(self.sql)
        result = cursor.fetchall()
        value_1 = []
        value_2 = []
        for item in result:
            value_1.append(item[0])
            value_2.append(item[1])
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=45)
        plt.bar(value_1,value_2)
        plt.savefig(f'static/{self.title}_bar.png')
        return plt.clf()


q = "SELECT recv_b, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM network ORDER BY updated DESC LIMIT 20;"
t = 'ram_u_vs_t'
b = CreatePlot(q, t)
b.ParamVsTime()


q2 = "SELECT sent_b, recv_b FROM network ORDER BY updated DESC LIMIT 20;"
t2 = 'test'
b2 = CreateBar(q2, t2)
b2.ParamVsParam()

q3 = "SELECT sent_b, recv_b FROM network ORDER BY updated DESC LIMIT 30;"
t3 = 'test2'
b2 = CreateBar(q3, t3)
b2.ParamVsParam()


