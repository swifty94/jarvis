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
from visualizer import *
from sql_strings import *
from bar import *
import mysql.connector
import logging
#####################
#
#   LOGGING PROPERTIES
#
#####################
FORMAT = '%(asctime)s   %(levelname)s   %(name)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)
#################
#
#   Application Routes
#
#################
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    header1 = GetSQLData(header_q1)
    header_result1 = header1.GetData()
    header2 = GetSQLData(header_q2)
    header_result2 = header2.GetData()
    sysinfo1 = GetSQLData(sysinfo_q1)
    sysinfo_result1 = sysinfo1.GetData()
    sysinfo2 = GetSQLData(sysinfo_q2)
    sysinfo_result2 = sysinfo2.GetData()
    cpu = VisualizeDataPie(cpu_q, cpu_l, cpu_t)
    net = VisualizeDataPie(net_p_q, net_p_l, net_p_t)
    netm = VisualizeDataPie(net_mb_q, net_mb_l, net_mb_t)
    ram = VisualizeDataPie(ram_q, ram_l, ram_t)
    disk = VisualizeDataPie(disk_q, disk_l, disk_t)
    swap = VisualizeDataPie(swap_q, swap_l, swap_t)
    cpu.CreatePieForTwo()
    net.CreatePieForTwo()
    netm.CreatePieForTwo()
    ram.CreatePieForThree()
    disk.CreatePieForThree()
    swap.CreatePieForThree()
    return render_template('index.html', header_result1=header_result1, sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2, header_result2=header_result2)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    header1 = GetSQLData(header_q1)
    header_result1 = header1.GetData()
    header2 = GetSQLData(header_q2)
    header_result2 = header2.GetData()
    sysinfo1 = GetSQLData(sysinfo_q1)
    sysinfo_result1 = sysinfo1.GetData()
    sysinfo2 = GetSQLData(sysinfo_q2)
    sysinfo_result2 = sysinfo2.GetData()
    cpu = VisualizeDataPie(cpu_q, cpu_l, cpu_t)
    net = VisualizeDataPie(net_p_q, net_p_l, net_p_t)
    netm = VisualizeDataPie(net_mb_q, net_mb_l, net_mb_t)
    ram = VisualizeDataPie(ram_q, ram_l, ram_t)
    disk = VisualizeDataPie(disk_q, disk_l, disk_t)
    swap = VisualizeDataPie(swap_q, swap_l, swap_t)
    cpu.CreatePieForTwo()
    net.CreatePieForTwo()
    netm.CreatePieForTwo()
    ram.CreatePieForThree()
    disk.CreatePieForThree()
    swap.CreatePieForThree()
    return render_template('index.html', header_result1=header_result1, sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2, header_result2=header_result2)

@app.route('/cpu_stats', methods=['POST', 'GET'])
def cpu_stats():
  cpu_f_vs_cpu_l()
  cpu_load_by_time()
  cpu_freq_by_time()
  cpu_table = GetSQLData(cpu_table_q)
  cpu_table_created = cpu_table.GetData()
  return render_template('cpu_stats.html',  cpu_table_created=cpu_table_created)

@app.route('/ram_stats', methods=['POST', 'GET'])
def ram_stats():
  ram_vs_time = VisualizePlotOrBar(ram_vs_time_q,ram_vs_time_t)
  ram_vs_time.ParamVsTime()
  ram_table = GetSQLData(ram_table_q)
  ram_table_created = ram_table.GetData()
  return render_template('ram_stats.html',  ram_table_created=ram_table_created)

@app.route('/disk_stats', methods=['POST', 'GET'])
def disk_stats():
  ParamVsTime(q2, t2)
  ParamVsTime(q3, t3)
  disk_table = GetSQLData(disk_table_q)
  disk_table_created = disk_table.GetData()
  return render_template('disk_stats.html',  disk_table_created=disk_table_created)

@app.route('/net_stats', methods=['POST', 'GET'])
def net_stats():
  ParamVsTime(q4, t4)
  ParamVsTime(q5, t5)
  net_table = GetSQLData(net_table_q)
  net_table_created = net_table.GetData()
  return render_template('net_stats.html',  net_table_created=net_table_created)

@app.route('/processes', methods=['POST', 'GET'])
def processes():
  import psutil
  names = []
  statuses = []
  cpus = []
  mems = []
  procs = psutil.pids()
  logging.info('Psutil Process handling started')
  for i in procs:
    try:
      p = psutil.Process(i)
      name = p.name()
      status = p.status()
      cpu = p.cpu_times()[1]        
      mem = round((p.memory_info()[1] / 1024 / 1024), 2)
      is_alive = p.is_running()
      if is_alive == True:
                if cpu > 1.0:
                    if mem > 1.0:
                      names.append(name)
                      statuses.append(status)
                      cpus.append(cpu)
                      mems.append(mem)                      
    except psutil.NoSuchProcess as nsp:
      pass
  result = list(zip(names,statuses,cpus,mems))
  result.sort(key=lambda x: x[2], reverse=True)
  logging.info('Successfully obtained Process object [names, statuses, cpu info, memory info]')
  return render_template('processes.html', result=result)

if __name__ == "__main__":
    try:
      app.logger.info('========= JARVIS SERVER STARTED ================')
      app.logger.info('========= version 1.0.0 ================')
      app.run(host='0.0.0.0',port=8081, debug=False)
    except Exception as E:
      app.logger.exception('ERROR. Caused by: {}'.format(E))
