import psutil
import platform
import time
from datetime import datetime

#   RAM data
svmem = psutil.virtual_memory()
swap = psutil.swap_memory()
swap_used = swap.used
swap_free = swap.free
avail_mem = svmem.available
used_mem = svmem.used

# CPU data
cpufreq = psutil.cpu_freq()
cur_freq = cpufreq.current
cpu_usage_t = psutil.cpu_percent(interval=0.1)
sensors_temp = psutil.sensors_temperatures()
coretemp_raw = sensors_temp["coretemp"]
temps = []
for x in coretemp_raw:
    temps.append(x[1])
coretemp = round(sum(temps) / len(temps), 2)

# Disk data
d = psutil.disk_usage('/')
d_used = d.used
d_free = d.free
disk_io = psutil.disk_io_counters()
read_io = disk_io.read_bytes
write_io = disk_io.write_bytes

# Network data
net_io = psutil.net_io_counters()
sent_b = net_io.bytes_sent
sent_p = net_io.packets_sent
recv_b = net_io.bytes_recv
recv_p = net_io.packets_recv

# General system data
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
boot_r = psutil.boot_time()
boot_h = datetime.fromtimestamp(boot_r)
d_total = d.total
swap_total = swap.total
total_mem = svmem.total