########################
#
#     Main graphical module for creating:
#       - pie charts 
#       - bar charts 
#       - static tables data 
#
#
########################
import time
import dateutil
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import mysql.connector
import logging

#####################
#
#   LOGGING PROPERTIES
#
#####################
FORMAT = '%(asctime)s   %(levelname)s   %(name)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)


###############
#
#   Class for creating matplotlib charts. Accepts SQL query, lable and title as the params. 
#
###############

class VisualizeDataPie():
    def __init__(self, sql, labels, title):
        self.sql = sql
        self.labels = labels
        self.title = title

    def CreatePieForTwo(self):
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'pyguard_v1',
        }
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        try:
            cursor.execute(self.sql)
            result = cursor.fetchall()
            x = []
            y = []
            for item in result:
                x.append(item[0])
                y.append(item[1])
            data = [x, y]
            colors = ['gold', 'yellowgreen']
            explode = (0.1, 0)
            labels = self.labels
            plt.pie(data, explode=explode, labels=labels, colors=colors,
                    shadow=True, autopct='%1.1f%%', startangle=100)
            plt.axis('equal')
            plt.legend(labels)
            plt.savefig(f'static/{self.title}_pie.png')
            logging.info('Successfully called VisualizeDataPie.CreatePieForTwo().')
            logging.info('SQL used [{}]'.format(self.sql))
            logging.info('Pie-chart <{}> created'.format(self.title))
        except Exception as e:
            logging.error('Failed to call VisualizeDataPie.CreatePieForTwo().')
            logging.error('SQL used [{}]'.format(self.sql))
            logging.info('Pie-chart <{}> not created'.format(self.title))
            logging.error('Full trace: {}'.format(e))
        cursor.close()
        return plt.clf()

    def CreatePieForThree(self):
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'pyguard_v1',
        }
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        try:
            cursor.execute(self.sql)
            result = cursor.fetchall()
            x = []
            y = []
            z = []
            for item in result:
                x.append(item[0])
                y.append(item[1])
                z.append(item[2])
            data = [x, y, z]
            colors = ['gold', 'yellowgreen', 'lightcoral']
            explode = (0, 0, 0.1)
            labels = self.labels
            plt.pie(data, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=100)
            plt.axis('equal')
            plt.savefig(f'static/{self.title}_pie.png')
            logging.info('Successfully called VisualizeDataPie.CreatePieForThree().')
            logging.info('SQL used [{}]'.format(self.sql))
            logging.info('Pie-chart <{}> created'.format(self.title))
        except Exception as e:
            logging.error('Failed to call VisualizeDataPie.CreatePieForThree().')
            logging.error('SQL used [{}]'.format(self.sql))
            logging.info('Pie-chart <{}> not created'.format(self.title))
            logging.error('Full trace: {}'.format(e))
        cursor.close()
        return plt.clf()


###############
#
#   Class for obtaining result by passing it SQL query as a param. 
#
###############

class GetSQLData():
    def __init__(self, sql):
        self.sql = sql

    def GetData(self):
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'pyguard_v1',
        }
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        try:
            cursor.execute(self.sql)
            result = cursor.fetchall()
            logging.info('Successfully called GetSQLData.GetData().')
            logging.info('SQL used [{}]'.format(self.sql))
        except Exception as e:
            logging.error('Failed to call GetSQLData.GetData().')
            logging.error('SQL used [{}]'.format(self.sql))
            logging.error('Full trace: {}'.format(e))
        cursor.close()
        return result


####################
#
#   Class for creating plots and bar charts. Accepts SQL query as a param
#
####################
class VisualizePlotOrBar():
    def __init__(self, sql, name):
        self.sql = sql
        self.name = name

    def ParamVsTime(self):
        param = []
        time = []
        get_sql = GetSQLData(self.sql)
        result = get_sql.GetData()
        for item in result:
            param.append(item[0])
            time.append(item[1])
        dates = [dateutil.parser.parse(s) for s in time]
        plt.subplots_adjust(bottom=0.3)
        plt.xticks(rotation=50)
        plt.title(self.name)
        ax = plt.gca()
        ax.set_xticks(dates)
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(dates, param)
        plt.savefig('static/{}.png'.format(self.name))
        return plt.clf()
