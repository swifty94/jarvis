###################################
#
#       DB connection properties
#
###################################
dbconfig = {
        'host':     '127.0.0.1',
        'user':     'jarvis',
        'password':  'jarvis',
        'database': 'jarvis',
        }
####################################################################
#
#   SQL queries for input data inserts (processed by sql_worker.py)
#
####################################################################
info_insert = """
REPLACE INTO sysinfo
SET id = 1,
osname = %s,
nodename = %s,
version = %s,
osarch = %s,
cpuarch = %s,
cores_ph = %s, 
cores_t = %s,
max_freq = %s, 
min_freq = %s, 
total_mem = %s, 
swap_total = %s, 
d_total = %s
"""
ram_insert = """INSERT INTO ram (avail_mem, used_mem, swap_used, swap_free) 
VALUES (%s, %s, %s, %s)"""

cpu_insert = """INSERT INTO cpu (cur_freq, cpu_percent, coretemp, boot, load_avg) 
VALUES (%s, %s, %s, %s, %s)"""

net_insert = """INSERT INTO network (sent_b, sent_p, recv_b, recv_p) 
VALUES (%s, %s, %s, %s)"""

disk_insert = """INSERT INTO disk (read_io, write_io, d_used, d_free) 
VALUES (%s, %s, %s, %s)"""

####################################################################################
#
#   SQL queries for the views in the UI interfase (processed by visualize_data.py)
#
####################################################################################
###########################################
#
#   SQL Queries for tables/cells/headers
#
###########################################
header_q1 = """
SELECT 
ROUND((SUM(c.cpu_percent)) / (COUNT(c.id)), 2) as 'CPU avg %',
ROUND((SUM(c.cur_freq)) / (COUNT(c.id)), 2) as 'CPU frequency avg in  GHz',
ROUND((SUM(r.used_mem)) / (COUNT(r.id)) /1024/1024/1024, 2) as 'RAM used avg in GB',
ROUND((SUM(r.swap_used)) / (COUNT(r.id)) /1024/1024/1024, 2) as 'SWAP used avg in GB'
FROM cpu c, ram r;"""
header_q2 = """
SELECT 
ROUND((SUM(d.read_io)) / (COUNT(d.id)) /1024/1024/1024, 2) as 'Read I/O avg in GB',
ROUND((SUM(d.write_io)) / (COUNT(d.id)) /1024/1024/1024, 2) as 'Write I/O avg in GB',
ROUND((SUM(n.sent_b)) / (COUNT(n.id)) /1024/1024/1024, 2) as 'Network - Sent avg in GB',
ROUND((SUM(n.recv_b)) / (COUNT(n.id)) /1024/1024/1024, 2) as 'Network - Received avg in GB'
FROM disk d, network n;"""
sysinfo_q1 = """
SELECT s.nodename, s.osname, s.osarch, s.cpuarch, c.boot FROM sysinfo s, cpu c ORDER BY c.updated DESC LIMIT 1;"""
sysinfo_q2 = """
SELECT ROUND(d_total / 1024 / 1024 / 1024) as total_space, 
ROUND(total_mem / 1024 / 1024 / 1024) as total_ram, 
ROUND(swap_total / 1024 / 1024 / 1024) as total_swap, cores_ph, 
cores_t, max_freq, min_freq 
FROM sysinfo ;"""
cpu_table_q = """
SELECT ROUND(cur_freq), 
cpu_percent, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM cpu 
WHERE DATE(updated) = curdate()
ORDER BY updated DESC;
"""
ram_table_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2),
ROUND(swap_used / 1024 / 1024, 2), 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM ram 
WHERE DATE(updated) = curdate()
ORDER BY updated DESC
"""
disk_table_q = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2),
ROUND(read_io / 1024 / 1024 / 1024, 2),
ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM disk
WHERE DATE(updated) = curdate()
ORDER BY updated DESC
"""
net_table_q = """
SELECT ROUND(sent_b / 1024 / 1024, 2),
ROUND(recv_b / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM network 
WHERE DATE(updated) = curdate()
ORDER BY updated DESC
"""

###########################################
#
#   SQL Queries for graphs
#
###########################################

#               RAM

ram_free_q = """
SELECT ROUND(avail_mem / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM ram
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
ram_free_vs_time_title = 'RAM free'
ram_free_vs_time_ylable = 'GB'


swap_free_q = """
SELECT ROUND(swap_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM ram
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
swap_free_vs_time_title = 'SWAP free'
swap_free_vs_time_ylable = 'GB'


ram_vs_time_q = """
SELECT ROUND(used_mem / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM ram 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
ram_vs_time_title = 'RAM usage'
ram_vs_time_ylable = 'GB'

swap_vs_time_q = """
SELECT ROUND(swap_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM ram 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
swap_vs_time_title = 'SWAP usage'
swap_vs_time_ylable = 'GB'



#               DISK

disk_used_q = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM disk 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
disk_used_vs_time_title = 'Occupied space'
disk_used_vs_time_ylable = 'GB'

disk_free_q = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM disk 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
disk_free_vs_time_title = 'Free space'
disk_free_vs_time_ylable = 'GB'

wio_vs_time_q = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM disk 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
wio_vs_time_title = 'Write GB from hard drive'
wio_vs_time_ylable = 'GB'



rio_vs_time_q = """
SELECT ROUND(read_io / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM disk 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
rio_vs_time_title = 'Read GB from hard drive'
rio_vs_time_ylable = 'GB'

#               NETWORK

sentb_vs_time_q = """
SELECT ROUND(sent_b / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM network 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
sentb_vs_time_title = 'Sent GB over network interfaces'
sentb_vs_time_ylable = 'GB'

resvb_vs_time_q = """
SELECT ROUND(recv_b / 1024 / 1024 / 1024, 2), 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') 
FROM network 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
resvb_vs_time_title = 'Received GB over network interfaces'
resvb_vs_time_ylable = 'GB'

net_sent_p_q = """
SELECT round(sent_p / 1000, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM network 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
net_sent_vs_time_title = 'Sent packets over network, K'
net_sent_vs_time_ylable = 'packets x 1000'


net_resv_q = """
SELECT round(recv_p / 1000, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM network 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
net_resv_vs_time_title = 'Received packets over network, K'
net_resv_vs_time_ylable = 'packets x 1000'

#                       CPU 

coretemp_vs_time_q = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM cpu
WHERE DATE(updated) = curdate()
ORDER BY updated ASC
"""
coretemp_vs_time_title = 'Average core temperature'
coretemp_vs_time_ylable = 'Temperature'

cpu_freq_vs_time_q = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM cpu 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC;
"""
cpu_freq_vs_time_title = 'CPU frequency'
cpu_freq_vs_time_ylable = 'GHz'

cpu_usage_t_vs_time_q = """
SELECT cpu_percent, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM cpu 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC;
"""
cpu_usage_t_vs_time_title = 'CPU % usage'
cpu_usage_t_vs_time_ylable = "% from 100"

loadavg_vs_time_q = """
SELECT load_avg,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i')
FROM cpu 
WHERE DATE(updated) = curdate()
ORDER BY updated ASC;
"""
loadavg_vs_time_title = 'CPU load avg. %'
loadavg_vs_time_ylable = "% from 100"

##############################
#
#   Queries for history data
#
#       for tables and graphs
#
#       (Current)
#
###############################

# Weekly
        # tables

cpu_history_w = """
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_percent as 'CPU  % ', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

ram_history_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""
disk_history_w = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""
net_history_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_w = """
SELECT cpu_percent, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

cpu_freq_vs_time_w = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

coretemp_vs_time_w = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

loadavg_vs_time_w = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

                # NETWORK

resvb_vs_time_w = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

sentb_vs_time_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

net_sent_p_w = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

net_resv_q_w = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

        # DISK


disk_used_w = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

disk_free_w = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

rio_vs_time_w = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

wio_vs_time_w = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

swap_vs_time_w = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

ram_vs_time_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""
swap_free_vs_time_w = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

ram_free_vs_time_w = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated ASC;
"""

# Monthly 

        # tables

cpu_history_m = """
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_percent as 'CPU  % ', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

ram_history_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""
disk_history_m = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""
net_history_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_m = """
SELECT cpu_percent,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

cpu_freq_vs_time_m = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

coretemp_vs_time_m = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

loadavg_vs_time_m = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

        # NETWORK

resvb_vs_time_m = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

sentb_vs_time_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

net_sent_p_m = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

net_resv_q_m = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

        # DISK

rio_vs_time_m = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

wio_vs_time_m = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

disk_used_m = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

disk_free_m = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

        # RAM

swap_vs_time_m = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

ram_vs_time_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

swap_free_vs_time_m = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""

ram_free_vs_time_m = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated ASC;
"""


##############################
#
#   Queries for history data
#
#       for tables and graphs
#
#       (Previous)
#
###############################

# Weekly
        # tables

cpu_history_wp = """
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_percent as 'CPU  % ', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

ram_history_wp = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""
disk_history_wp = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""
net_history_wp = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM network 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_wp = """
SELECT cpu_percent, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

cpu_freq_vs_time_wp = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

coretemp_vs_time_wp = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

loadavg_vs_time_wp = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

                # NETWORK

resvb_vs_time_wp = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

sentb_vs_time_wp = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

net_sent_p_wp = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

net_resv_q_wp = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

        # DISK


disk_used_wp = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

disk_free_wp = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

rio_vs_time_wp = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

wio_vs_time_wp = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

swap_vs_time_wp = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

ram_vs_time_wp = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""
swap_free_vs_time_wp = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

ram_free_vs_time_wp = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE week(updated) = week(curdate())-1
ORDER BY updated ASC;
"""

# Monthly 

        # tables

cpu_history_mp = """
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_percent as 'CPU  % ', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

ram_history_mp = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""
disk_history_mp = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""
net_history_mp = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_mp = """
SELECT cpu_percent,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

cpu_freq_vs_time_mp = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

coretemp_vs_time_mp = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

loadavg_vs_time_mp = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

        # NETWORK

resvb_vs_time_mp = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

sentb_vs_time_mp = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

net_sent_p_mp = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

net_resv_q_mp = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

        # DISK

rio_vs_time_mp = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

wio_vs_time_mp = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

disk_used_mp = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

disk_free_mp = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

        # RAM

swap_vs_time_mp = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

ram_vs_time_mp = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

swap_free_vs_time_mp = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""

ram_free_vs_time_mp = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())-1
ORDER BY updated ASC;
"""