##############################################################################
#
#     Main web-server module
#
#     Requests routing depending on regular HTTP request from browser
#
#     Serving matplotlib and database content on fly
#
##############################################################################
from flask import Flask, request, render_template, redirect, url_for, session
import requests
from waitress import serve
from multiprocessing import Pool
import logging
from visualize_data import *
from sql_strings import *
####################################################
#
#   Logging properties
#
####################################################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)
####################################################
#
#  Psutil-based 'top'-like monitor/task mngr.
#
#####################################################
def process_monitor():
    import psutil
    names = []
    paths = []
    cpus = []
    mems = []
    logging.info('JARVIS: jarvis -> process_monitor() START \n')
    procs = psutil.pids()
    for i in procs:
        try:
            p = psutil.Process(i)
            name = p.name()
            path = p.exe()
            cpu = p.cpu_percent(interval=0.05)
            mem = round((p.memory_info()[1] / 1024 / 1024), 2)
            if p.is_running() == True:
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
    logging.info('JARVIS: jarvis -> process_monitor() FINISH \n')
    result.sort(key=lambda x: x[2], reverse=True)
    return result
##########################################
#
#   Application URLs
#
##########################################
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
    response.cache_control.max_age = 50
    return response

@app.context_processor
def header_data():
    sysinfo_result1 = get_sql_data(sysinfo_q1)
    sysinfo_result2 = get_sql_data(sysinfo_q2)
    try:
        logging.info('JARVIS:  context_processor -> refreshing Jinja template cache  \n')
        return dict(sysinfo_result1=sysinfo_result1, sysinfo_result2=sysinfo_result2)
    except Exception as e:
        logging.error('JARVIS: context_processor -> FAILED to refresh Jinja template \n')
        logging.error(f'JARVIS: caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
        logging.info('JARVIS:  context_processor -> Jinja template cache refreshed \n')

@app.route('/', methods=['POST', 'GET'])
def index():
    ram_vs_time = _pool.apply_async(single_kpi_now, (ram_vs_time_q, ram_vs_time_title, ram_vs_time_ylable, ))
    swap_vs_time = _pool.apply_async(single_kpi_now, (swap_vs_time_q, swap_vs_time_title, swap_vs_time_ylable, ))
    ram_free_vs_time = _pool.apply_async(single_kpi_now, (ram_free_q, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
    swap_free_vs_time = _pool.apply_async(single_kpi_now, (swap_free_q, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
    coretemp = _pool.apply_async(single_kpi_now, (coretemp_vs_time_q, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
    cpu_usage_vs_time = _pool.apply_async(single_kpi_now, (cpu_usage_t_vs_time_q, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
    cpu_freq_vs_time = _pool.apply_async(single_kpi_now, (cpu_freq_vs_time_q, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
    loadavg = _pool.apply_async(single_kpi_now, (loadavg_vs_time_q, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
    disk_free = _pool.apply_async(single_kpi_now, (disk_free_q, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
    disk_used = _pool.apply_async(single_kpi_now, (disk_used_q, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
    disk_w = _pool.apply_async(single_kpi_now, (wio_vs_time_q, wio_vs_time_title, wio_vs_time_ylable, ))
    disk_r = _pool.apply_async(single_kpi_now, (rio_vs_time_q, rio_vs_time_title, rio_vs_time_ylable, ))
    sentb_vs_time = _pool.apply_async(single_kpi_now, (sentb_vs_time_q, sentb_vs_time_title, sentb_vs_time_ylable, ))
    resvb_vs_time = _pool.apply_async(single_kpi_now, (resvb_vs_time_q, resvb_vs_time_title, resvb_vs_time_ylable, ))
    sentp_vs_time = _pool.apply_async(single_kpi_now, (net_sent_p_q, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
    resvp_vs_time = _pool.apply_async(single_kpi_now, (net_resv_q, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
    header_result1 = get_sql_data(header_q1)
    header_result2 = get_sql_data(header_q2)
    try:
      logging.info('JARVIS: received HTTP request for "/" \n')
      return render_template('index.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get(), disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get(), sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get(), header_result1=header_result1, header_result2=header_result2)
    except Exception as e:
      logging.error('JARVIS: FAILED to process HTTP request for /dashboard STATUS: 500 Internal Server Error \n')
      logging.error(f'JARVIS: caught exception [ {e} ]')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
      logging.info('JARVIS: HTTP request for "/" DONE. Session closed \n')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    ram_vs_time = _pool.apply_async(single_kpi_now, (ram_vs_time_q, ram_vs_time_title, ram_vs_time_ylable, ))
    swap_vs_time = _pool.apply_async(single_kpi_now, (swap_vs_time_q, swap_vs_time_title, swap_vs_time_ylable, ))
    ram_free_vs_time = _pool.apply_async(single_kpi_now, (ram_free_q, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
    swap_free_vs_time = _pool.apply_async(single_kpi_now, (swap_free_q, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
    coretemp = _pool.apply_async(single_kpi_now, (coretemp_vs_time_q, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
    cpu_usage_vs_time = _pool.apply_async(single_kpi_now, (cpu_usage_t_vs_time_q, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
    cpu_freq_vs_time = _pool.apply_async(single_kpi_now, (cpu_freq_vs_time_q, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
    loadavg = _pool.apply_async(single_kpi_now, (loadavg_vs_time_q, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
    disk_free = _pool.apply_async(single_kpi_now, (disk_free_q, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
    disk_used = _pool.apply_async(single_kpi_now, (disk_used_q, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
    disk_w = _pool.apply_async(single_kpi_now, (wio_vs_time_q, wio_vs_time_title, wio_vs_time_ylable, ))
    disk_r = _pool.apply_async(single_kpi_now, (rio_vs_time_q, rio_vs_time_title, rio_vs_time_ylable, ))
    sentb_vs_time = _pool.apply_async(single_kpi_now, (sentb_vs_time_q, sentb_vs_time_title, sentb_vs_time_ylable, ))
    resvb_vs_time = _pool.apply_async(single_kpi_now, (resvb_vs_time_q, resvb_vs_time_title, resvb_vs_time_ylable, ))
    sentp_vs_time = _pool.apply_async(single_kpi_now, (net_sent_p_q, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
    resvp_vs_time = _pool.apply_async(single_kpi_now, (net_resv_q, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
    header_result1 = get_sql_data(header_q1)
    header_result2 = get_sql_data(header_q2)
    try:
      logging.info('JARVIS: received HTTP request for /dashboard \n')
      return render_template('index.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get(), disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get(), sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get(), header_result1=header_result1, header_result2=header_result2)
    except Exception as e:
      logging.error('JARVIS: FAILED to process HTTP request for /dashboard STATUS: 500 Internal Server Error \n')
      logging.error(f'JARVIS: caught exception [ {e} ]')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    finally:
      logging.info('JARVIS: HTTP request for /dashboard DONE. Session closed \n')

@app.route('/cpu_stats', methods=['POST', 'GET'])
def cpu_stats():
  coretemp = _pool.apply_async(single_kpi_now, (coretemp_vs_time_q, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
  cpu_usage_vs_time = _pool.apply_async(single_kpi_now, (cpu_usage_t_vs_time_q, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
  cpu_freq_vs_time = _pool.apply_async(single_kpi_now, (cpu_freq_vs_time_q, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
  loadavg = _pool.apply_async(single_kpi_now, (loadavg_vs_time_q, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
  cpu_table_created = get_sql_data(cpu_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /cpu_stats \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created,coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /cpu_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /cpu_stats DONE. Session closed \n')

@app.route('/cpu_week', methods=['POST', 'GET'])
def cpu_week():
  coretemp = _pool.apply_async(single_kpi_week, (coretemp_vs_time_w, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
  cpu_usage_vs_time = _pool.apply_async(single_kpi_week, (cpu_usage_t_vs_time_w, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
  cpu_freq_vs_time = _pool.apply_async(single_kpi_week, (cpu_freq_vs_time_w, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
  loadavg = _pool.apply_async(single_kpi_week, (loadavg_vs_time_w, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
  cpu_table_created = get_sql_data(cpu_history_w)
  try:
    logging.info('JARVIS: /cpu_stats -> single_kpi_week() -> weekly report generation... \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created, coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for weekly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /cpu_stats -> single_kpi_week() -> report generation DONE. Session closed \n')

@app.route('/cpu_month', methods=['POST', 'GET'])
def cpu_month():
  coretemp = _pool.apply_async(single_kpi_month, (coretemp_vs_time_m, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
  cpu_usage_vs_time = _pool.apply_async(single_kpi_month, (cpu_usage_t_vs_time_m, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
  cpu_freq_vs_time = _pool.apply_async(single_kpi_month, (cpu_freq_vs_time_m, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
  loadavg = _pool.apply_async(single_kpi_month, (loadavg_vs_time_m, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
  cpu_table_created = get_sql_data(cpu_history_m)
  try:
    logging.info('JARVIS: /cpu_stats -> cpu_month() -> monthly report generation... \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created, coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for monthly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /cpu_stats -> cpu_month() -> monthly report generation DONE. Session closed \n')

@app.route('/cpu_week_prev', methods=['POST', 'GET'])
def cpu_week_prev():
  coretemp = _pool.apply_async(single_kpi_week, (coretemp_vs_time_wp, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
  cpu_usage_vs_time = _pool.apply_async(single_kpi_week, (cpu_usage_t_vs_time_wp, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
  cpu_freq_vs_time = _pool.apply_async(single_kpi_week, (cpu_freq_vs_time_wp, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
  loadavg = _pool.apply_async(single_kpi_week, (loadavg_vs_time_wp, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
  cpu_table_created = get_sql_data(cpu_history_wp)
  try:
    logging.info('JARVIS: /cpu_week_prev -> single_kpi_week() -> weekly report generation... \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created, coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for weekly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /cpu_week_prev -> single_kpi_week() -> report generation DONE. Session closed \n')

@app.route('/cpu_month_prev', methods=['POST', 'GET'])
def cpu_month_prev():
  coretemp = _pool.apply_async(single_kpi_month, (coretemp_vs_time_mp, coretemp_vs_time_title, coretemp_vs_time_ylable, ))
  cpu_usage_vs_time = _pool.apply_async(single_kpi_month, (cpu_usage_t_vs_time_mp, cpu_usage_t_vs_time_title, cpu_usage_t_vs_time_ylable, ))
  cpu_freq_vs_time = _pool.apply_async(single_kpi_month, (cpu_freq_vs_time_mp, cpu_freq_vs_time_title, cpu_freq_vs_time_ylable, ))
  loadavg = _pool.apply_async(single_kpi_month, (loadavg_vs_time_mp, loadavg_vs_time_title, loadavg_vs_time_ylable, ))
  cpu_table_created = get_sql_data(cpu_history_mp)
  try:
    logging.info('JARVIS: /cpu_month_prev -> single_kpi_month() -> monthly report generation... \n')
    return render_template('cpu_stats.html', cpu_table_created=cpu_table_created, coretemp=coretemp.get(), cpu_usage_vs_time=cpu_usage_vs_time.get(), cpu_freq_vs_time=cpu_freq_vs_time.get(), loadavg=loadavg.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for monthly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /cpu_month_prev -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

@app.route('/ram_stats', methods=['POST', 'GET'])
def ram_stats():
  ram_vs_time = _pool.apply_async(single_kpi_now, (ram_vs_time_q, ram_vs_time_title, ram_vs_time_ylable, ))
  swap_vs_time = _pool.apply_async(single_kpi_now, (swap_vs_time_q, swap_vs_time_title, swap_vs_time_ylable, ))
  ram_free_vs_time = _pool.apply_async(single_kpi_now, (ram_free_q, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
  swap_free_vs_time = _pool.apply_async(single_kpi_now, (swap_free_q, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
  ram_table_created = get_sql_data(ram_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /ram_stats \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /ram_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /ram_stats DONE. Session closed \n')

@app.route('/ram_week', methods=['POST', 'GET'])
def ram_week():
  ram_vs_time = _pool.apply_async(single_kpi_week, (ram_vs_time_w, ram_vs_time_title, ram_vs_time_ylable, ))
  swap_vs_time = _pool.apply_async(single_kpi_week, (swap_vs_time_w, swap_vs_time_title, swap_vs_time_ylable, ))
  ram_free_vs_time = _pool.apply_async(single_kpi_week, (ram_free_vs_time_w, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
  swap_free_vs_time = _pool.apply_async(single_kpi_week, (swap_free_vs_time_w, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
  ram_table_created = get_sql_data(ram_history_w)
  try:
    logging.info('JARVIS: /ram_stats -> single_kpi_week() -> monthly report generation... \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for weekly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /ram_stats -> single_kpi_week() -> report generation DONE. Session closed \n')

@app.route('/ram_month', methods=['POST', 'GET'])
def ram_month():
  ram_vs_time = _pool.apply_async(single_kpi_month, (ram_vs_time_m, ram_vs_time_title, ram_vs_time_ylable, ))
  swap_vs_time = _pool.apply_async(single_kpi_month, (swap_vs_time_m, swap_vs_time_title, swap_vs_time_ylable, ))
  ram_free_vs_time = _pool.apply_async(single_kpi_month, (ram_free_vs_time_m, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
  swap_free_vs_time = _pool.apply_async(single_kpi_month, (swap_free_vs_time_m, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
  ram_table_created = get_sql_data(ram_history_m)
  try:
    logging.info('JARVIS: /ram_stats -> single_kpi_month() -> monthly report generation... \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for monthly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /ram_stats -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

@app.route('/ram_week_prev', methods=['POST', 'GET'])
def ram_week_prev():
  ram_vs_time = _pool.apply_async(single_kpi_week, (ram_vs_time_wp, ram_vs_time_title, ram_vs_time_ylable, ))
  swap_vs_time = _pool.apply_async(single_kpi_week, (swap_vs_time_wp, swap_vs_time_title, swap_vs_time_ylable, ))
  ram_free_vs_time = _pool.apply_async(single_kpi_week, (ram_free_vs_time_wp, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
  swap_free_vs_time = _pool.apply_async(single_kpi_week, (swap_free_vs_time_wp, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
  ram_table_created = get_sql_data(ram_history_wp)
  try:
    logging.info('JARVIS: /ram_week_prev -> single_kpi_week() -> monthly report generation... \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for weekly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /ram_week_prev -> single_kpi_week() -> report generation DONE. Session closed \n')

@app.route('/ram_month_prev', methods=['POST', 'GET'])
def ram_month_prev():
  ram_vs_time = _pool.apply_async(single_kpi_month, (ram_vs_time_mp, ram_vs_time_title, ram_vs_time_ylable, ))
  swap_vs_time = _pool.apply_async(single_kpi_month, (swap_vs_time_mp, swap_vs_time_title, swap_vs_time_ylable, ))
  ram_free_vs_time = _pool.apply_async(single_kpi_month, (ram_free_vs_time_mp, ram_free_vs_time_title, ram_free_vs_time_ylable, ))
  swap_free_vs_time = _pool.apply_async(single_kpi_month, (swap_free_vs_time_mp, swap_free_vs_time_title, swap_free_vs_time_ylable, ))
  ram_table_created = get_sql_data(ram_history_mp)
  try:
    logging.info('JARVIS: /ram_month_prev -> single_kpi_month() -> monthly report generation... \n')
    return render_template('ram_stats.html', ram_vs_time=ram_vs_time.get(), swap_vs_time=swap_vs_time.get(), swap_free_vs_time=swap_free_vs_time.get(), ram_free_vs_time=ram_free_vs_time.get(), ram_table_created=ram_table_created)
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for monthly report generation \n STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ]')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /ram_month_prev -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

@app.route('/disk_stats', methods=['POST', 'GET'])
def disk_stats():
  disk_free = _pool.apply_async(single_kpi_now, (disk_free_q, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
  disk_used = _pool.apply_async(single_kpi_now, (disk_used_q, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
  disk_w = _pool.apply_async(single_kpi_now, (wio_vs_time_q, wio_vs_time_title, wio_vs_time_ylable, ))
  disk_r = _pool.apply_async(single_kpi_now, (rio_vs_time_q, rio_vs_time_title, rio_vs_time_ylable, ))
  disk_table_created = get_sql_data(disk_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /disk_stats \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /disk_stats DONE. Session closed \n')

@app.route('/disk_week', methods=['POST', 'GET'])
def disk_week():
  disk_free = _pool.apply_async(single_kpi_week, (disk_free_w, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
  disk_used = _pool.apply_async(single_kpi_week, (disk_used_w, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
  disk_w = _pool.apply_async(single_kpi_week, (wio_vs_time_w, wio_vs_time_title, wio_vs_time_ylable, ))
  disk_r = _pool.apply_async(single_kpi_week, (rio_vs_time_w, rio_vs_time_title, rio_vs_time_ylable, ))
  disk_table_created = get_sql_data(disk_history_m)
  try:
    logging.info('JARVIS: /disk_stats -> single_kpi_week() -> weekly report generation... \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /disk_stats -> single_kpi_week() -> weekly report generation DONE. Session closed \n')

@app.route('/disk_month', methods=['POST', 'GET'])
def disk_month():
  disk_free = _pool.apply_async(single_kpi_month, (disk_free_m, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
  disk_used = _pool.apply_async(single_kpi_month, (disk_used_m, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
  disk_w = _pool.apply_async(single_kpi_month, (wio_vs_time_m, wio_vs_time_title, wio_vs_time_ylable, ))
  disk_r = _pool.apply_async(single_kpi_month, (rio_vs_time_m, rio_vs_time_title, rio_vs_time_ylable, ))
  disk_table_created = get_sql_data(disk_history_m)
  try:
    logging.info('JARVIS: /disk_stats -> single_kpi_month() -> monthly report generation... \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /disk_stats -> single_kpi_month() -> monthly report generation DONE. Session closed \n')


@app.route('/disk_week_prev', methods=['POST', 'GET'])
def disk_week_prev():
  disk_free = _pool.apply_async(single_kpi_week, (disk_free_wp, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
  disk_used = _pool.apply_async(single_kpi_week, (disk_used_wp, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
  disk_w = _pool.apply_async(single_kpi_week, (wio_vs_time_wp, wio_vs_time_title, wio_vs_time_ylable, ))
  disk_r = _pool.apply_async(single_kpi_week, (rio_vs_time_wp, rio_vs_time_title, rio_vs_time_ylable, ))
  disk_table_created = get_sql_data(disk_history_wp)
  try:
    logging.info('JARVIS: /disk_week_prev -> single_kpi_week() -> weekly report generation... \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_week_prev STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /disk_week_prev -> single_kpi_week() -> weekly report generation DONE. Session closed \n')

@app.route('/disk_month_prev', methods=['POST', 'GET'])
def disk_month_prev():
  disk_free = _pool.apply_async(single_kpi_month, (disk_free_mp, disk_free_vs_time_title, disk_free_vs_time_ylable, ))
  disk_used = _pool.apply_async(single_kpi_month, (disk_used_mp, disk_used_vs_time_title, disk_used_vs_time_ylable, ))
  disk_w = _pool.apply_async(single_kpi_month, (wio_vs_time_mp, wio_vs_time_title, wio_vs_time_ylable, ))
  disk_r = _pool.apply_async(single_kpi_month, (rio_vs_time_mp, rio_vs_time_title, rio_vs_time_ylable, ))
  disk_table_created = get_sql_data(disk_history_mp)
  try:
    logging.info('JARVIS: /disk_month_prev -> single_kpi_month() -> monthly report generation... \n')
    return render_template('disk_stats.html',  disk_table_created=disk_table_created, disk_free=disk_free.get(), disk_used=disk_used.get(), disk_w=disk_w.get(), disk_r=disk_r.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /disk_month_prev STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /disk_month_prev -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

@app.route('/net_stats', methods=['POST', 'GET'])
def net_stats():
  sentb_vs_time = _pool.apply_async(single_kpi_now, (sentb_vs_time_q, sentb_vs_time_title, sentb_vs_time_ylable, ))
  resvb_vs_time = _pool.apply_async(single_kpi_now, (resvb_vs_time_q, resvb_vs_time_title, resvb_vs_time_ylable, ))
  sentp_vs_time = _pool.apply_async(single_kpi_now, (net_sent_p_q, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
  resvp_vs_time = _pool.apply_async(single_kpi_now, (net_resv_q, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
  net_table_created = get_sql_data(net_table_q)
  try:
    logging.info('JARVIS: received HTTP request for /net_stats \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: HTTP request for /net_stats DONE. Session closed \n')


@app.route('/net_week', methods=['POST', 'GET'])
def net_week():
  sentb_vs_time = _pool.apply_async(single_kpi_week, (sentb_vs_time_w, sentb_vs_time_title, sentb_vs_time_ylable, ))
  resvb_vs_time = _pool.apply_async(single_kpi_week, (resvb_vs_time_w, resvb_vs_time_title, resvb_vs_time_ylable, ))
  sentp_vs_time = _pool.apply_async(single_kpi_week, (net_sent_p_w, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
  resvp_vs_time = _pool.apply_async(single_kpi_week, (net_resv_q_w, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
  net_table_created = get_sql_data(net_history_m)
  try:
    logging.info('JARVIS: /net_stats -> single_kpi_week() -> weekly report generation... \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_stats STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /net_stats -> single_kpi_week() -> weekly report generation DONE. Session closed \n')


@app.route('/net_month', methods=['POST', 'GET'])
def net_month():
  sentb_vs_time = _pool.apply_async(single_kpi_month, (sentb_vs_time_m, sentb_vs_time_title, sentb_vs_time_ylable, ))
  resvb_vs_time = _pool.apply_async(single_kpi_month, (resvb_vs_time_m, resvb_vs_time_title, resvb_vs_time_ylable, ))
  sentp_vs_time = _pool.apply_async(single_kpi_month, (net_sent_p_m, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
  resvp_vs_time = _pool.apply_async(single_kpi_month, (net_resv_q_m, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
  net_table_created = get_sql_data(net_history_m)
  try:
    logging.info('JARVIS: /net_stats -> single_kpi_month() -> monthly report generation... \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_month STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /net_stats -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

@app.route('/net_week_prev', methods=['POST', 'GET'])
def net_week_prev():
  sentb_vs_time = _pool.apply_async(single_kpi_week, (sentb_vs_time_wp, sentb_vs_time_title, sentb_vs_time_ylable, ))
  resvb_vs_time = _pool.apply_async(single_kpi_week, (resvb_vs_time_wp, resvb_vs_time_title, resvb_vs_time_ylable, ))
  sentp_vs_time = _pool.apply_async(single_kpi_week, (net_sent_p_wp, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
  resvp_vs_time = _pool.apply_async(single_kpi_week, (net_resv_q_wp, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
  net_table_created = get_sql_data(net_history_wp)
  try:
    logging.info('JARVIS: /net_week_prev -> single_kpi_week() -> weekly report generation... \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_week_prev STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /net_week_prev -> single_kpi_week() -> weekly report generation DONE. Session closed \n')


@app.route('/net_month_prev', methods=['POST', 'GET'])
def net_month_prev():
  sentb_vs_time = _pool.apply_async(single_kpi_month, (sentb_vs_time_mp, sentb_vs_time_title, sentb_vs_time_ylable, ))
  resvb_vs_time = _pool.apply_async(single_kpi_month, (resvb_vs_time_mp, resvb_vs_time_title, resvb_vs_time_ylable, ))
  sentp_vs_time = _pool.apply_async(single_kpi_month, (net_sent_p_mp, net_sent_vs_time_title, net_sent_vs_time_ylable, ))
  resvp_vs_time = _pool.apply_async(single_kpi_month, (net_resv_q_mp, net_resv_vs_time_title, net_resv_vs_time_ylable, ))
  net_table_created = get_sql_data(net_history_mp)
  try:
    logging.info('JARVIS: /net_month_prev -> single_kpi_month() -> monthly report generation... \n')
    return render_template('net_stats.html',  net_table_created=net_table_created, sentb_vs_time=sentb_vs_time.get(), resvb_vs_time=resvb_vs_time.get(), sentp_vs_time=sentp_vs_time.get(), resvp_vs_time=resvp_vs_time.get())
  except Exception as e:
    logging.error('JARVIS: FAILED to process HTTP request for /net_month_prev STATUS: 500 Internal Server Error \n')
    logging.error(f'JARVIS: caught exception [ {e} ] \n')
    logging.error('JARVIS: Full trace: \n', exc_info=1)
  finally:
    logging.info('JARVIS: /net_month_prev -> single_kpi_month() -> monthly report generation DONE. Session closed \n')

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
    logging.info('JARVIS: HTTP request for /processes DONE. Session closed \n')

if __name__ == "__main__":
    try:
      _pool = Pool(processes=5)
      logging.info('========= JARVIS SERVER START ============= \n')
      logging.info('========= JARVIS Pool Initialized ============= \n')
      serve(app, host='0.0.0.0', port=5000)
    except OSError as ose:
      logging.error('======== FAIL ========')
      logging.error(f'======== JARVIS: Caught exception [ {ose} ] ======== \n')
      logging.info('========= JARVIS Pool Initialization FAILED ============= \n')
      logging.error('JARVIS: Full trace: \n', exc_info=1)
    except Exception as e:
      logging.error('======== FAIL ======== \n')
      logging.error(f'======== JARVIS: Caught exception [ {e} ] ======== \n')
      logging.info('========= JARVIS Pool Initialization FAILED ============= \n')
      logging.error('JARVIS: Full trace: \n', exc_info=1)