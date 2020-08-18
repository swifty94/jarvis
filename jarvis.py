##########################
#
#     Main web-server module
#
#     Requests routing depending on regular HTTP request from UI
#     based on mysql, matplotlib, flask and python 3, self api
#
##########################
from flask import Flask, request, render_template, redirect, url_for, session
import requests
from visual_worker import *
from sql_strings import *
import mysql.connector
import logging
#####################
#
#   LOGGING PROPERTIES
#
#####################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)
#################
#
#   Application Routes
#
#################
app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 15
    #response.cache_control.no-store        failed so far, // todo: 500 custom page
    return response

@app.route('/debug_ui', methods=['POST', 'GET'])
def debug():
  return render_template('base.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    header_result1 = get_sql_data(header_q1)
    header_result2 = get_sql_data(header_q2)
    sysinfo_result1 = get_sql_data(sysinfo_q1)
    sysinfo_result2 = get_sql_data(sysinfo_q2)
    pie_for_three(disk_q, disk_label, disk_title, disk_name)
    pie_for_three(ram_q, ram_label, ram_title, ram_name)
    pie_for_three(swap_q, swap_label, swap_title, swap_name)
    pie_for_two(cpu_q, cpu_label, cpu_title, cpu_name)
    pie_for_two(net_p_q, net_p_label, net_p_title, net_p_name)
    pie_for_two(net_mb_q, net_mb_label, net_mb_title, net_mb_name)
    return render_template('index.html', header_result1=header_result1, sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2, header_result2=header_result2)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    header_result1 = get_sql_data(header_q1)
    header_result2 = get_sql_data(header_q2)
    sysinfo_result1 = get_sql_data(sysinfo_q1)
    sysinfo_result2 = get_sql_data(sysinfo_q2)
    pie_for_three(disk_q, disk_label, disk_title, disk_name)
    pie_for_three(ram_q, ram_label, ram_title, ram_name)
    pie_for_three(swap_q, swap_label, swap_title, swap_name)
    pie_for_two(cpu_q, cpu_label, cpu_title, cpu_name)
    pie_for_two(net_p_q, net_p_label, net_p_title, net_p_name)
    pie_for_two(net_mb_q, net_mb_label, net_mb_title, net_mb_name)
    return render_template('index.html', header_result1=header_result1, sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2, header_result2=header_result2)

@app.route('/cpu_stats', methods=['POST', 'GET'])
def cpu_stats():
  param_vs_time_graph(coretemp_vs_time_q, coretemp_vs_time_name, coretemp_vs_time_title, coretemp_vs_time_ylable, coretemp_vs_time_xlable)
  param_vs_time_graph(cpu_usage_t_vs_time_q, cpu_usage_t_vs_time_name, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, cpu_usage_t_vs_time_xlable)
  param_vs_time_graph(cpu_freq_vs_time_q, cpu_freq_vs_time_name, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, cpu_freq_vs_time_xlable)
  cpu_table_created = get_sql_data(cpu_table_q)
  return render_template('cpu_stats.html',  cpu_table_created=cpu_table_created)

@app.route('/ram_stats', methods=['POST', 'GET'])
def ram_stats():
  param_vs_time_graph(ram_vs_time_q, ram_vs_time_name, ram_vs_time_title, ram_vs_time_ylable, ram_vs_time_xlable)
  pie_for_three(ram_q, ram_label, ram_title, ram_name)
  pie_for_three(swap_q, swap_label, swap_title, swap_name)
  ram_table_created = get_sql_data(ram_table_q)
  return render_template('ram_stats.html',  ram_table_created=ram_table_created)

@app.route('/disk_stats', methods=['POST', 'GET'])
def disk_stats():
  pie_for_three(disk_q, disk_label, disk_title, disk_name)
  param_vs_time_graph(wio_vs_time_q, wio_vs_time_name, wio_vs_time_title, wio_vs_time_ylable, wio_vs_time_xlable)
  param_vs_time_graph(rio_vs_time_q, rio_vs_time_name, rio_vs_time_title, rio_vs_time_ylable, rio_vs_time_xlable)
  disk_table_created = get_sql_data(disk_table_q)
  return render_template('disk_stats.html',  disk_table_created=disk_table_created)

@app.route('/net_stats', methods=['POST', 'GET'])
def net_stats():
  param_vs_time_graph(sentb_vs_time_q, sentb_vs_time_name, sentb_vs_time_title, sentb_vs_time_ylable, sentb_vs_time_xlable)
  param_vs_time_graph(resvb_vs_time_q, resvb_vs_time_name, resvb_vs_time_title, resvb_vs_time_ylable, resvb_vs_time_xlable)
  pie_for_two(net_p_q, net_p_label, net_p_title, net_p_name)
  pie_for_two(net_mb_q, net_mb_label, net_mb_title, net_mb_name)
  net_table_created = get_sql_data(net_table_q)
  return render_template('net_stats.html',  net_table_created=net_table_created)

@app.route('/processes', methods=['POST', 'GET'])
def processes():
  def process_monitor():
    import psutil
    names = []
    paths = []
    cpus = []
    mems = []
    logging.info('JARVIS: Call process_monitor() START')
    procs = psutil.pids()
    for i in procs:
        try:
            p = psutil.Process(i)
            name = p.name()
            path = p.exe()
            cpu = p.cpu_times()[1]        
            mem = round((p.memory_info()[1] / 1024 / 1024), 2)
            is_alive = p.is_running()
            if is_alive == True:
                if cpu > 1.0:
                    if mem > 1.0:
                        names.append(name)
                        paths.append(path)
                        cpus.append(cpu)
                        mems.append(mem)
        except psutil.NoSuchProcess as nsp:
            pass
        except psutil.AccessDenied as ad:
            pass
        except Exception as e:
            logging.error(f'JARVIS: Caught exception [ {e} ]')
            logging.error('JARVIS: Full trace: \n', exc_info=1)

    result = list(zip(names,paths,cpus,mems))
    logging.info('JARVIS: Call process_monitor() FINISH')
    result.sort(key=lambda x: x[2], reverse=True)
    return result
   
  result = process_monitor()
  return render_template('processes.html', result=result)

if __name__ == "__main__":
    try:
      app.logger.info('======== JARVIS SERVER STARTED ========')
      app.logger.info('======== version 1.0.2 ========')
      app.run(host='0.0.0.0',port=8080, debug=False)
    except OSError as ose:
      app.logger.error('======== FAIL ========')
      app.logger.error(f'======== JARVIS: Caught exception [ {ose} ] ========')
      app.logger.error('JARVIS: Full trace: \n', exc_info=1)
    except Exception as e:
      app.logger.error('======== FAIL ========')
      app.logger.error(f'======== JARVIS: Caught exception [ {e} ] ========')
      app.logger.error('JARVIS: Full trace: \n', exc_info=1)
