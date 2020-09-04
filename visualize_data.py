import matplotlib as mpl
mpl.use ( 'Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
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

def single_kpi_now(sql, title, ylable):
    """
    Function for creating matplotlib plot chart with correlation between parameter and time
    Accepting sql query, labels, title and name.
    On call taking the variables defined in sql_stnings.py

    Return the Base64 encoded image rendered on fly to Jinja2 template.

    Example:

    single_kpi_now(some_qeury, some_label, some_title, some_name)
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
    xfmt = md.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_major_locator(md.MinuteLocator(interval=5))
    plt.plot(dates,param)
    plt.tight_layout()
    try:
        plt.savefig(img, format='png')
        param_vs_time_graph = base64.b64encode(img.getvalue()).decode()
        img.seek(0)
        logging.info(f'JARVIS: visual_worker -> single_kpi_now() \n Created [ {title} ] plot graph \n')
        plt.clf()
        return param_vs_time_graph
    except Exception as e:
        logging.error(f'JARVIS: FAILED to call visual_worker -> single_kpi_now() caught exception [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)


def single_kpi_week(sql, title, ylable):
    """
    Inheriting main functionality from single_kpi_now() but with date formating and location
    relevant for weekly statistics.

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
    xfmt = md.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=(MO, TU, WE, TH, FR, SA, SU), interval=1))
    plt.plot(dates,param)
    plt.tight_layout()
    try:
        plt.savefig(img, format='png')
        param_vs_time_graph = base64.b64encode(img.getvalue()).decode()
        img.seek(0)
        logging.info(f'JARVIS: visual_worker -> single_kpi_week() \n Created [ {title} ] plot graph \n')
        plt.clf()
        return param_vs_time_graph
    except Exception as e:
        logging.error(f'JARVIS: FAILED to call visual_worker -> single_kpi_week() caught exception [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)

def single_kpi_month(sql, title, ylable):
    """
    Inheriting main functionality from single_kpi_now() but with date formating and location
    relevant for weekly statistics.

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
    xfmt = md.DateFormatter('%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_major_locator(md.DayLocator(bymonthday=range(1,32)))
    plt.plot(dates,param)
    plt.tight_layout()
    try:
        plt.savefig(img, format='png')
        param_vs_time_graph = base64.b64encode(img.getvalue()).decode()
        img.seek(0)
        return param_vs_time_graph
    except Exception as e:
        logging.error(f'JARVIS: FAILED to call visual_worker -> single_kpi_month() caught exception [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
        logging.info(f'JARVIS: visual_worker -> single_kpi_month() \n Created [ {title} ] plot graph \n')
        plt.clf()