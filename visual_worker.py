import matplotlib as mpl
mpl.use ( 'Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import io
import os
import time
from time import time
import base64
import mysql.connector
import dateutil
import logging
from datetime import datetime
from sql_strings import dbconfig
##########################
#
#   LOGGING PROPERTIES
#
##########################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)
###################################
#
#   Function performace wrapper
#
###################################
def performance(fn):
  def wrapper(*args, **kwargs):
    start = time()
    result = fn(*args, **kwargs)
    end = time()
    delta = round((end - start), 4)
    out = {
        'Function':     fn.__name__,
        'Time, sec': delta,
    }
    logging.info(f'JARVIS: @performace.wrapper() \n {out} \n')
    return result
  return wrapper
#################################
#
#   Main visualization functions
#
#################################

@performance
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
            logging.info(f'JARVIS: visual_worker -> get_sql_fetchone() \n SQL used  {sql} \n')
            return result
            cursor.close()
        except Exception as e:
            logging.error(f'JARVIS: FAILED to call visual_worker -> get_sql_fetchone() \n SQL used {sql} \n')
            logging.error(f'JARVIS: get_sql_data() caught exception [ {e} ]')
            logging.error('JARVIS: Full trace: \n', exc_info=1)
            cursor.close()

@performance
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
        result = cursor.fetchone()
        logging.info(f'JARVIS: visual_worker.get_sql_fetchone() \n SQL used {sql} \n')
        return result
        cursor.close()
    except Exception as e:
        logging.error(f'JARVIS: FAILED to call visual_worker.get_sql_fetchone() \n SQL used {sql} \n')
        logging.error(f'JARVIS: visual_worker.get_sql_fetchone() caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
        cursor.close()

def param_vs_time_graph(sql, title, ylable):
    """
    Function for creating matplotlib plot chart with correlation between parameter and time
    Accepting sql query, labels, title and name.
    On call taking the variables defined in sql_stnings.py

    Return the Base64 encoded image to Jinja2 template.

    Example:

    param_vs_time_graph(some_qeury, some_label, some_title, some_name)
    """
    img = io.BytesIO()
    result = get_sql_data(sql)
    param = []
    time = []
    for item in result:
        param.append(item[0])
        time.append(item[1])
    dates = [dateutil.parser.parse(s) for s in time]
    plt.subplots_adjust(wspace=0.2, bottom=0.5)
    plt.subplots(figsize=(10,3.5))
    plt.xticks(rotation=50)
    plt.title(title)
    plt.ylabel(ylable, fontsize=12)
    ax=plt.gca()
    ax.tick_params(direction='out', length=3, width=1, color='r')
    ax.set_xticks(dates)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,param)
    plt.tight_layout()
    try:
        plt.savefig(img, format='png')
        param_vs_time_graph = base64.b64encode(img.getvalue()).decode()
        img.seek(0)
        logging.info(f'JARVIS: visual_worker -> param_vs_time_graph() \n Created [ {title} ] plot graph \n')
        plt.clf()
        return param_vs_time_graph
    except Exception as e:
        logging.error(f'JARVIS: FAILED to call visual_worker -> param_vs_time_graph() caught exception [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)