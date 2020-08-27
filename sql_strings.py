##################################
#
#       DB connection properties
#
##################################
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
#   SQL queries for the views in the UI interfase (processed by visual_worker.py)
#
####################################################################################
#################################
#
#   SQL Queries for charts
#
################################

#               RAM

ram_free_q = """
SELECT ROUND(avail_mem / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram
ORDER by updated 
DESC LIMIT 7;
"""
ram_free_vs_time_title = 'RAM free'
ram_free_vs_time_ylable = 'Megabytes'
ram_free_vs_time_xlable = 'Date and time'


swap_free_q = """
SELECT ROUND(swap_free / 1024 / 1024 / 1024, 2) Available_SWAP, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram
ORDER by updated 
DESC LIMIT 7;"""
swap_free_vs_time_title = 'SWAP free'
swap_free_vs_time_ylable = 'Megabytes'
swap_free_vs_time_xlable = 'Date and time'


ram_vs_time_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
ORDER by updated 
DESC LIMIT 7;
"""
ram_vs_time_title = 'RAM usage'
ram_vs_time_ylable = 'Megabytes'
ram_vs_time_xlable = 'Date and time'

swap_vs_time_q = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
ORDER by updated 
DESC LIMIT 7;
"""
swap_vs_time_title = 'SWAP usage'
swap_vs_time_ylable = 'Megabytes'
swap_vs_time_xlable = 'Date and time'



#               DISK

disk_used_q = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
ORDER by updated 
DESC LIMIT 7;
"""
disk_used_vs_time_title = 'Occupied space'
disk_used_vs_time_ylable = 'Megabytes'
disk_used_vs_time_xlable = 'Date and time'

disk_free_q = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
ORDER by updated 
DESC LIMIT 7;
"""
disk_free_vs_time_title = 'Free space'
disk_free_vs_time_ylable = 'Megabytes'
disk_free_vs_time_xlable = 'Date and time'

wio_vs_time_q = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
ORDER by updated 
DESC LIMIT 7;
"""
wio_vs_time_title = 'Write MB from hard drive'
wio_vs_time_ylable = 'Megabytes'
wio_vs_time_xlable = 'Date and time'


rio_vs_time_q = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM disk 
ORDER by updated DESC LIMIT 7;
"""
rio_vs_time_title = 'Read MB from hard drive'
rio_vs_time_ylable = 'Megabytes'
rio_vs_time_xlable = 'Date and time'

#               NETWORK

sentb_vs_time_q = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 7;
"""
sentb_vs_time_title = 'Sent MB over network interfaces'
sentb_vs_time_ylable = 'Megabytes'
sentb_vs_time_xlable = 'Date and time'

resvb_vs_time_q = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 7;
"""
resvb_vs_time_title = 'Received MB over network interfaces'
resvb_vs_time_ylable = 'Megabytes'
resvb_vs_time_xlable = 'Date and time'

net_sent_p_q = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
ORDER by updated 
DESC LIMIT 7;
"""
net_sent_vs_time_title = 'Sent packets over network'
net_sent_vs_time_ylable = '№ of packets'
net_sent_vs_time_xlable = 'Date and time'


net_resv_q = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
ORDER by updated 
DESC LIMIT 7;
"""
net_resv_vs_time_title = 'Received packets over network'
net_resv_vs_time_ylable = '№ of packets'
net_resv_vs_time_xlable = 'Date and time'

#                       CPU 

coretemp_vs_time_q = """
SELECT coretemp, DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' FROM cpu ORDER BY updated DESC LIMIT 7;"""
coretemp_vs_time_title = 'Average core temperature'
coretemp_vs_time_ylable = 'Temperature'
coretemp_vs_time_xlable = 'Date and time'

cpu_freq_vs_time_q = """
SELECT cur_freq, DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' FROM cpu ORDER BY updated DESC LIMIT 7;
"""
cpu_freq_vs_time_title = 'CPU frequency'
cpu_freq_vs_time_ylable = 'Hz'
cpu_freq_vs_time_xlable = 'Date and time'

cpu_usage_t_vs_time_q = """
SELECT cpu_percent, DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' FROM cpu ORDER BY updated DESC LIMIT 7;
"""
cpu_usage_t_vs_time_title = 'CPU % usage'
cpu_usage_t_vs_time_ylable = "% from 100"
cpu_usage_t_vs_time_xlable = 'Date and time'

loadavg_vs_time_q = """
SELECT cpu_percent, DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' FROM cpu ORDER BY updated DESC LIMIT 7;
"""
loadavg_vs_time_title = 'CPU load avg. %'
loadavg_vs_time_ylable = "% from 100"
loadavg_vs_time_xlable = 'Date and time'

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
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_percent as 'CPU  % ', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
ORDER by updated DESC LIMIT 10;
"""
ram_table_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
ORDER BY updated DESC 
LIMIT 10;
"""
disk_table_q = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
updated as 'Date'
FROM disk
ORDER BY updated 
DESC LIMIT 10;
"""
net_table_q = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
ORDER by updated DESC LIMIT 10;
"""

##############################
#
#   Queries for history data
#
#       for tables and graphs
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
ORDER BY updated
DESC LIMIT 100;
"""

ram_history_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
disk_history_w = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
net_history_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE' 
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_w = """
SELECT cpu_percent, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

cpu_freq_vs_time_w = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

coretemp_vs_time_w = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

loadavg_vs_time_w = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

                # NETWORK

resvb_vs_time_w = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

sentb_vs_time_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

net_sent_p_w = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

net_resv_q_w = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

        # DISK


disk_used_w = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

disk_free_w = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

rio_vs_time_w = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

wio_vs_time_w = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;"""

swap_vs_time_w = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

ram_vs_time_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""
swap_free_vs_time_w = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

ram_free_vs_time_w = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 20;
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
ORDER BY updated
DESC LIMIT 100;
"""

ram_history_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
disk_history_m = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
net_history_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 100;
"""
        # graphs

                # CPU

cpu_usage_t_vs_time_m = """
SELECT cpu_percent,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

cpu_freq_vs_time_m = """
SELECT cur_freq, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;
"""

coretemp_vs_time_m = """
SELECT coretemp, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;"""

loadavg_vs_time_m = """
SELECT load_avg, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;"""

        # NETWORK

resvb_vs_time_m = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;"""

sentb_vs_time_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 20;"""

net_sent_p_m = """
SELECT sent_p AS Sent_packets, 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

net_resv_q_m = """
SELECT recv_p AS Received_packets,
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

        # DISK

rio_vs_time_m = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;"""

wio_vs_time_m = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

disk_used_m = """
SELECT ROUND(d_used / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

disk_free_m = """
SELECT ROUND(d_free / 1024 / 1024 / 1024, 2),
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

        # RAM

swap_vs_time_m = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

ram_vs_time_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

swap_free_vs_time_m = """
SELECT ROUND(swap_free / 1024 / 1024, 2) as 'Free SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""

ram_free_vs_time_m = """
SELECT ROUND(avail_mem / 1024 / 1024, 2) as 'Free RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d %H:%i') as 'DATE'
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 15;
"""