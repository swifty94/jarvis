import psutil
import platform
import time
import logging
from datetime import datetime
from visualize_data import performance

FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)

#   RAM data
@performance
def get_ram():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    swap_used = swap.used
    swap_free = swap.free
    avail_mem = svmem.available
    used_mem = svmem.used
    try:
        logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): swap: used,free ram:avail, used \n')
        return swap_used, swap_free, avail_mem, used_mem
    except Exception as e:
        logging.error(f'JARVIS: Caught system_data_kpi in get_ram() ->  [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)


# CPU data
@performance
def get_cpu():
    cpufreq = psutil.cpu_freq()
    cur_freq = cpufreq.current
    cpu_percent = psutil.cpu_percent(interval=None)
    boot_r = psutil.boot_time()
    boot_h = datetime.fromtimestamp(boot_r)
    loadavg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()][0]
    if hasattr(psutil, "sensors_temperatures"):
        sensors_temp = psutil.sensors_temperatures()
        logging.info(f'JARVIS INFO: system_data_kpi() -> psutil -> sensors_temperatures() SUPPORTED \n')
        if "coretemp" in sensors_temp:
            coretemp_raw = sensors_temp["coretemp"]
            temps = []
            for x in coretemp_raw:
                temps.append(x[1])
                coretemp = round(sum(temps) / len(temps), 2)
                try:
                    logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): cpu: freq, percent, coretemp, boot, loadavgv \n')
                    return cur_freq, cpu_percent, coretemp, boot_h, loadavg
                except Exception as e:
                    logging.error(f'JARVIS: Caught system_data_kpi in get_cpu() ->  [ {e} ] \n')
                    logging.error('JARVIS: Full trace: \n', exc_info=1)
        else:
            coretemp = 0
            logging.info(f'JARVIS INFO: system_data_kpi() -> psutil -> sensors_temperatures() -> sensors_temp no coretemp key \n (CPU temperature = 0) \n')
    else:
        coretemp = 0
        logging.info(f'JARVIS INFO: system_data_kpi() -> psutil -> sensors_temperatures() NOT SUPPORTED \n All sensor values = 0 \n')
        try:
            logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): cpu: freq, percent, coretemp, boot, loadavgv \n')
            return cur_freq, cpu_percent, coretemp, boot_h, loadavg
        except Exception as e:
            logging.error(f'JARVIS: Caught system_data_kpi in get_cpu() ->  [ {e} ] \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)


# Disk data
@performance
def get_disk():
    d = psutil.disk_usage('/')
    d_used = d.used
    d_free = d.free
    disk_io = psutil.disk_io_counters()
    read_io = disk_io.read_bytes
    write_io = disk_io.write_bytes
    try:
        logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): disk: used/free space, read/write speed \n')
        return d_used, d_free, read_io, write_io
    except Exception as e:
        logging.error(f'JARVIS: Caught system_data_kpi in get_disk() ->  [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
    

# Network data
@performance
def get_net():
    net_io = psutil.net_io_counters()
    sent_b = net_io.bytes_sent
    sent_p = net_io.packets_sent
    recv_b = net_io.bytes_recv
    recv_p = net_io.packets_recv
    try:
        logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): network: sent/recv bytes/packets\n')
        return sent_b, sent_p, recv_b, recv_p
    except Exception as e:
        logging.error(f'JARVIS: Caught system_data_kpi in get_net() ->  [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)

# General system data
@performance
def get_sys():
    d = psutil.disk_usage('/')
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpufreq = psutil.cpu_freq()
    uname = platform.uname()
    osname = uname.system
    nodename = uname.node
    release = uname.release
    version = uname.version
    osarch = uname.machine
    cpuarch = uname.processor
    cores_ph = psutil.cpu_count(logical=False)
    cores_t = psutil.cpu_count(logical=True)
    max_freq = cpufreq.max
    min_freq = cpufreq.min
    d_total = d.total
    swap_total = swap.total
    total_mem = svmem.total
    try:
        logging.info(f'JARVIS INFO: Processing:  system_data_kpi(): sys: refresh static data \n')
        return osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total
    except Exception as e:
        logging.error(f'JARVIS: Caught system_data_kpi in get_sys() ->  [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
