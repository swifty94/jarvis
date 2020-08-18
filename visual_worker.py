import matplotlib as mpl
mpl.use ( 'Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
from datetime import datetime
from sql_strings import dbconfig
import mysql.connector
import os
import logging
#####################
#
#   LOGGING PROPERTIES
#
#####################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)


def get_sql_data(sql):
        """
        Function for multi-row data fetch from the MySQL. 
        Accepting sql query as the parameter.

        Example:

        result = get_sql_data(sql)
        """
        try:
            mydb = mysql.connector.connect(**dbconfig)
            cursor = mydb.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            logging.info('JARVIS: OK call get_sql_data()')
            logging.info(f'SQL used [{sql}]')
            return result
            cursor.close()
        except Exception as e:
            logging.error(f'JARVIS: FAIL call get_sql_data()')
            logging.error(f'SQL used [{sql}]')
            logging.error(f'JARVIS: Caught exception [ {e} ]')
            logging.error('JARVIS: Full trace: \n', exc_info=1)
            cursor.close()

def get_sql_fetchone(sql):
    """
    Function for single row data fetch from the MySQL.
    Accepting sql query as the parameter.

    Example:

    result = get_sql_fetchone(sql)
    """
    try:
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = list(cursor.fetchone())
        logging.info('JARVIS: OK call get_sql_fetchone()')
        logging.info(f'SQL used [{sql}]')
        return result
        cursor.close()
    except Exception as e:
        logging.error(f'JARVIS: FAIL call get_sql_fetchone()')
        logging.error(f'SQL used [{sql}]')
        logging.error(f'JARVIS: Caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
        cursor.close()

def pie_for_three(sql, labels, title, name):
    """
    Function for creating matplotlib pie chart with 3 slices
    Accepting sql query, labels, title and name.
    On call taking the variables defined in sql_stnings.py

    Example:

    pie_for_three(some_qeury, some_label, some_title, some_name)
    """
    result = get_sql_fetchone(sql)
    data = result
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.1, 0, 0)
    labels = labels
    plt.title(title, y=1.05)
    plt.pie(data, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=60)
    plt.axis('equal')
    try:
        plt.savefig(f'static/{name}_pie.png')
        logging.info('JARVIS: OK call pie_for_three()')
        logging.info(f'JARVIS: Created [ {name} ] pie chart')
        return plt.clf()
    except Exception as e:
        logging.error('JARVIS: FAIL call pie_for_three()')
        logging.error(f'JARVIS: Caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
    
def pie_for_two(sql, labels, title, name):
    """
    Function for creating matplotlib pie chart with 2 slices
    Accepting sql query, labels, title and name.
    On call taking the variables defined in sql_stnings.py

    Example:

    pie_for_two(some_qeury, some_label, some_title, some_name)
    """
    result = get_sql_fetchone(sql)
    data = result
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0)
    labels = labels
    plt.title(title, y=1.05)
    plt.pie(data, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=60)
    plt.axis('equal')
    try:
        plt.savefig(f'static/{name}_pie.png')
        logging.info('JARVIS: OK call pie_for_two()')
        logging.info(f'JARVIS: Created [ {name} ] pie chart')
        return plt.clf()
    except Exception as e:
        logging.error('JARVIS: FAIL call pie_for_two()')
        logging.error(f'JARVIS: Caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)

def param_vs_time_graph(sql, name, title, ylable, xlable):
    """
    Function for creating matplotlib plot chart with correlation between parameter and time
    Accepting sql query, labels, title and name.
    On call taking the variables defined in sql_stnings.py

    Example:

    pie_for_two(some_qeury, some_label, some_title, some_name)
    """
    result = get_sql_data(sql)
    param = []
    time = []
    for item in result:
        param.append(item[0])
        time.append(item[1])
    dates = [dateutil.parser.parse(s) for s in time]
    plt.subplots_adjust(wspace=0.1, bottom=0.4)
    plt.xticks(rotation=50)
    plt.title(title)
    plt.ylabel(ylable, fontsize=12)
    plt.xlabel(xlable, fontsize=12)
    ax=plt.gca()
    ax.set_xticks(dates)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,param)
    try:
        plt.savefig(f'static/{name}.png')
        logging.info('JARVIS: Call param_vs_time_graph()')
        logging.info(f'JARVIS: Created [ {name} ] plot graph')
        return plt.clf()
    except Exception as e:
        logging.error('JARVIS: FAIL call param_vs_time_graph()')
        logging.error(f'JARVIS: Caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)