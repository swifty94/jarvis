##########################
#
#     Main web-server module
#
#     Requests routing depending on regular HTTP request from UI
#
#     Serving matplotlib and database content on fly
#
##########################
# public modules import
from flask import Flask, request, render_template, redirect, url_for, session
import requests
from waitress import serve
from multiprocessing import Pool
import logging
# inner modules import
from visual_worker import *
from sql_strings import *
##########################
#
#   LOGGING PROPERTIES
#
##########################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)
############################
#
#  Unix 'top'-like monitor
#
############################
def process_monitor():
    import psutil
    names = []
    paths = []
    cpus = []
    mems = []
    logging.info('JARVIS: jarvis.process_monitor() START \n')
    procs = psutil.pids()
    for i in procs:
        try:
            p = psutil.Process(i)
            name = p.name()
            path = p.exe()
            cpu = p.cpu_percent(interval=0.1)
            mem = round((p.memory_info()[1] / 1024 / 1024), 2)
            if p.is_running() == True:
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
            logging.error(f'JARVIS: Caught exception [ {e} ] \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)

    result = list(zip(names,paths,cpus,mems))
    logging.info('JARVIS: jarvis.process_monitor() FINISH \n')
    result.sort(key=lambda x: x[2], reverse=True)
    return result
#####################
#
#   Main web-server 
#
#####################
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 500

@app.after_request
def add_header(response):
    response.cache_control.max_age = 90
    return response

@app.context_processor
def header_data():
    header_result1 = get_sql_data(header_q1)
    header_result2 = get_sql_data(header_q2)
    sysinfo_result1 = get_sql_data(sysinfo_q1)
    sysinfo_result2 = get_sql_data(sysinfo_q2)
    return dict(header_result1=header_result1, header_result2=header_result2, sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2)

@app.route('/', methods=['POST', 'GET'])
def index():
    disk = _pool.apply_async(pie_for_three, (disk_q, disk_label, disk_title, ))
    ram = _pool.apply_async(pie_for_three, (ram_q, ram_label, ram_title, ))
    swap = _pool.apply_async(pie_for_three, (swap_q, swap_label, swap_title, ))
    cpu = _pool.apply_async(pie_for_two, (cpu_q, cpu_label, cpu_title, ))
    net_p = _pool.apply_async(pie_for_two, (net_p_q, net_p_label, net_p_title, ))
    net_mb = _pool.apply_async(pie_for_two, (net_mb_q, net_mb_label, net_mb_title, ))
    try:
      logging.info('JARVIS: received HTTP request for /dashboard \n')
      return render_template('index.html', disk=disk.get(), ram=ram.get(), swap=swap.get(), cpu=cpu.get(), net_p=net_p.get(), net_mb=net_mb.get())
    except Exception as e:
      logging.error('JARVIS: FAILED to process HTTP request for /dashboard STATUS: 500 Internal Server Error \n')
      logging.error(f'JARVIS: caught exception [ {e} ]')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
      logging.info('JARVIS: HTTP request for /dashboard STATUS: 200 OK \n')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    disk = _pool.apply_async(pie_for_three, (disk_q, disk_label, disk_title, ))
    ram = _pool.apply_async(pie_for_three, (ram_q, ram_label, ram_title, ))
    swap = _pool.apply_async(pie_for_three, (swap_q, swap_label, swap_title, ))
    cpu = _pool.apply_async(pie_for_two, (cpu_q, cpu_label, cpu_title, ))
    net_p = _pool.apply_async(pie_for_two, (net_p_q, net_p_label, net_p_title, ))
    net_mb = _pool.apply_async(pie_for_two, (net_mb_q, net_mb_label, net_mb_title, ))
    try:
      logging.info('JARVIS: received HTTP request for /dashboard \n')
      return render_template('index.html', disk=disk.get(), ram=ram.get(), swap=swap.get(), cpu=cpu.get(), net_p=net_p.get(), net_mb=net_mb.get())
    except Exception as e:
      logging.error('JARVIS: FAILED to process HTTP request for /dashboard STATUS: 500 Internal Server Error \n')
      logging.error(f'JARVIS: caught exception [ {e} ]')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
      logging.info('JARVIS: HTTP request for /dashboard STATUS: 200 OK \n')

@app.route('/cpu_stats', methods=['POST', 'GET'])
def cpu_stats():
  coretemp = _pool.apply_async(param_vs_time_graph, (coretemp_vs_time_q, coretemp_vs_time_title, coretemp_vs_time_ylable, coretemp_vs_time_xlable, ))
  cpu_usage_vs_time = _pool.apply_async(param_vs_time_graph, (cpu_usage_t_vs_time_q, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, cpu_usage_t_vs_time_xlable, ))
  cpu_freq_vs_time = _pool.apply_async(param_vs_time_graph, (cpu_freq_vs_time_q, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, cpu_freq_vs_time_xlable, ))
  cpu = _pool.apply_async(pie_for_two, (cpu_q, cpu_label, cpu_title, ))
  cpu_table_created = get_sql_data(cpu_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /cpu_stats \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created, coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), cpu=cpu.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /cpu_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /cpu_stats STATUS: 200 OK \n')

@app.route('/ram_stats', methods=['POST', 'GET'])
def ram_stats():
  ram_vs_time = _pool.apply_async(param_vs_time_graph, (ram_vs_time_q, ram_vs_time_title, ram_vs_time_ylable, ram_vs_time_xlable, ))
  swap_vs_time = _pool.apply_async(param_vs_time_graph, (swap_vs_time_q, swap_vs_time_title, swap_vs_time_ylable, swap_vs_time_xlable, ))
  ram = _pool.apply_async(pie_for_three, (ram_q, ram_label, ram_title, ))
  swap = _pool.apply_async(pie_for_three, (swap_q, swap_label, swap_title, ))
  ram_table_created = get_sql_data(ram_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /ram_stats \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap=swap.get(), ram=ram.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /ram_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /ram_stats STATUS: 200 OK \n')

@app.route('/disk_stats', methods=['POST', 'GET'])
def disk_stats():
  disk = _pool.apply_async(pie_for_three, (disk_q, disk_label, disk_title, ))
  disk_w = _pool.apply_async(param_vs_time_graph, (wio_vs_time_q, wio_vs_time_title, wio_vs_time_ylable, wio_vs_time_xlable, ))
  disk_r = _pool.apply_async(param_vs_time_graph, (rio_vs_time_q, rio_vs_time_title, rio_vs_time_ylable, rio_vs_time_xlable))
  disk_table_created = get_sql_data(disk_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /disk_stats \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk=disk.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /disk_stats STATUS: 200 OK \n')

@app.route('/net_stats', methods=['POST', 'GET'])
def net_stats():
  sentb_vs_time = _pool.apply_async(param_vs_time_graph, (sentb_vs_time_q, sentb_vs_time_title, sentb_vs_time_ylable, sentb_vs_time_xlable, ))
  resvb_vs_time = _pool.apply_async(param_vs_time_graph, (resvb_vs_time_q, resvb_vs_time_title, resvb_vs_time_ylable, resvb_vs_time_xlable, ))
  net_p = _pool.apply_async(pie_for_two, (net_p_q, net_p_label, net_p_title, ))
  net_mb = _pool.apply_async(pie_for_two, (net_mb_q, net_mb_label, net_mb_title, ))
  net_table_created = get_sql_data(net_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /net_stats \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), net_p=net_p.get(), net_mb=net_mb.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /net_stats STATUS: 200 OK \n')

@app.route('/processes', methods=['POST', 'GET'])
def processes():
  result = _pool.apply_async(process_monitor, ())
  try:
    logging.info('JARVIS: received HTTP request for /processes \n')
    return render_template('processes.html', result=result.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /processes STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /processes STATUS: 200 OK \n')

if __name__ == "__main__":
    try:
      _pool = Pool(processes=5)
      logging.info('========= JARVIS SERVER START ============= \n')
      serve(app, host='0.0.0.0', port=8080)
    except OSError as ose:
      logging.error('======== FAIL ========')
      logging.error(f'======== JARVIS: Caught exception [ {ose} ] ======== \n')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    except Exception as e:
      logging.error('======== FAIL ======== \n')
      logging.error(f'======== JARVIS: Caught exception [ {e} ] ======== \n')
      logging.error('JARVIS: Full trace: \n', exc_info=1)