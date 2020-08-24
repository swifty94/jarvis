import psutil
import platform
import time
from datetime import datetime

#   RAM data
def get_ram():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    swap_used = swap.used
    swap_free = swap.free
    avail_mem = svmem.available
    used_mem = svmem.used
    return swap_used, swap_free, avail_mem, used_mem

# CPU data
def get_cpu():
    cpufreq = psutil.cpu_freq()
    cur_freq = cpufreq.current
    cpu_usage_t = psutil.cpu_percent(interval=0.1)
    boot_r = psutil.boot_time()
    boot_h = datetime.fromtimestamp(boot_r)
    sensors_temp = psutil.sensors_temperatures()
    coretemp_raw = sensors_temp["coretemp"]
    temps = []
    for x in coretemp_raw:
        temps.append(x[1])
    coretemp = round(sum(temps) / len(temps), 2)
    return cur_freq, cpu_usage_t, coretemp, boot_h

# Disk data
def get_disk():
    d = psutil.disk_usage('/')
    d_used = d.used
    d_free = d.free
    disk_io = psutil.disk_io_counters()
    read_io = disk_io.read_bytes
    write_io = disk_io.write_bytes
    return d_used, d_free, read_io, write_io

# Network data
def get_net():
    net_io = psutil.net_io_counters()
    sent_b = net_io.bytes_sent
    sent_p = net_io.packets_sent
    recv_b = net_io.bytes_recv
    recv_p = net_io.packets_recv
    return sent_b, sent_p, recv_b, recv_p

# General system data
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
    return osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total

