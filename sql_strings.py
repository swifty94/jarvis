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

cpu_insert = """INSERT INTO cpu (cur_freq, cpu_usage_t, coretemp, boot) 
VALUES (%s, %s, %s, %s)"""

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
#   SQL Queries for charts/pies
#
################################
cpu_q = """
SELECT ROUND(c.cur_freq)as Current_frequency_MHz, 
ROUND(s.max_freq) as MAX_frequency_MHz 
FROM cpu c, sysinfo s 
ORDER BY c.updated 
DESC LIMIT 1;"""
cpu_label = 'Current','MAX'
cpu_title = 'MAX and MIN CPU frequency'


net_p_q = """
SELECT sent_p AS Sent_packets, 
recv_p AS Received_packets 
FROM network 
ORDER BY updated 
DESC LIMIT 1;"""
net_p_label = 'Sent packets', 'Received packets'
net_p_title = 'Amount of sent vs received packets over network'

net_mb_q = """
SELECT ROUND(sent_b / 1024 / 1024 ) Sent_MB, 
ROUND(recv_b / 1024 / 1024 ) Received_MB 
FROM network 
ORDER by updated 
DESC LIMIT 1;"""
net_mb_label = 'Sent MB', 'Received MB'
net_mb_title = 'Amount of sent vs received MB over network'

ram_q = """
SELECT ROUND(s.total_mem / 1024 / 1024 / 1024, 2) Total_RAM, 
ROUND(r.avail_mem / 1024 / 1024 / 1024, 2) Available_RAM, 
ROUND(r.used_mem / 1024 / 1024 / 1024, 2) Used_RAM  
FROM sysinfo s, ram r 
ORDER by r.updated 
DESC LIMIT 1;"""
ram_label = 'Total', 'Available', 'Used'
ram_title = 'RAM memory usage'

disk_q = """
SELECT ROUND(s.d_total / 1024 / 1024 / 1024, 2) Total, 
ROUND(d.d_used / 1024 / 1024 / 1024, 2) Used, 
ROUND(d.d_free / 1024 / 1024 / 1024, 2) Free 
FROM sysinfo s, disk d 
ORDER by d.updated 
DESC LIMIT 1;"""
disk_label = 'Total', 'Available', 'Used'
disk_title = 'Hard drive space consumption'

swap_q = """
SELECT ROUND(s.swap_total / 1024 / 1024 / 1024, 2) Total_SWAP, 
ROUND(r.swap_free / 1024 / 1024 / 1024, 2) Available_SWAP, 
ROUND(r.swap_used / 1024 / 1024 / 1024, 2) Used_SWAP  
FROM sysinfo s, ram r 
ORDER by r.updated 
DESC LIMIT 1;"""
swap_label = 'Total', 'Available', 'Used'
swap_title = 'Swap memory usage'


ram_vs_time_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
ORDER by updated 
DESC LIMIT 10;
"""
ram_vs_time_title = 'RAM usage'
ram_vs_time_ylable = 'Megabytes'
ram_vs_time_xlable = 'Date and time'

swap_vs_time_q = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
ORDER by updated 
DESC LIMIT 10;
"""
swap_vs_time_title = 'SWAP usage'
swap_vs_time_ylable = 'Megabytes'
swap_vs_time_xlable = 'Date and time'


wio_vs_time_q = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
ORDER by updated 
DESC LIMIT 10;"""
wio_vs_time_title = 'Write MB from hard drive'
wio_vs_time_ylable = 'Megabytes'
wio_vs_time_xlable = 'Date and time'


rio_vs_time_q = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
ORDER by updated DESC LIMIT 10;"""
rio_vs_time_title = 'Read MB from hard drive'
rio_vs_time_ylable = 'Megabytes'
rio_vs_time_xlable = 'Date and time'

sentb_vs_time_q = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 10;"""
sentb_vs_time_title = 'Sent MB over network interfaces'
sentb_vs_time_ylable = 'Megabytes'
sentb_vs_time_xlable = 'Date and time'

resvb_vs_time_q = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 10;"""
resvb_vs_time_title = 'Received MB over network interfaces'
resvb_vs_time_ylable = 'Megabytes'
resvb_vs_time_xlable = 'Date and time'

coretemp_vs_time_q = """
SELECT coretemp, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM cpu ORDER BY updated DESC LIMIT 10;"""
coretemp_vs_time_title = 'Average core temperature'
coretemp_vs_time_ylable = 'Temperature'
coretemp_vs_time_xlable = 'Date and time'

cpu_freq_vs_time_q = """
SELECT cur_freq, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM cpu ORDER BY updated DESC LIMIT 10;
"""
cpu_freq_vs_time_title = 'CPU frequency'
cpu_freq_vs_time_ylable = 'Hz'
cpu_freq_vs_time_xlable = 'Date and time'

cpu_usage_t_vs_time_q = """
SELECT cpu_usage_t, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM cpu ORDER BY updated DESC LIMIT 10;
"""
cpu_usage_t_vs_time_title = 'CPU load'
cpu_usage_t_vs_time_ylable = "% from 100"
cpu_usage_t_vs_time_xlable = 'Date and time'

###########################################
#
#   SQL Queries for tables/cells/headers
#
###########################################
header_q1 = """
SELECT 
ROUND((SUM(c.cpu_usage_t)) / (COUNT(c.id)), 2) as 'CPU avg %',
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
cpu_usage_t as 'CPU load % ', 
updated as 'DATE' 
FROM cpu 
ORDER by updated DESC LIMIT 10;
"""
ram_table_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
updated as 'DATE' 
FROM ram ORDER BY updated DESC LIMIT 10;
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
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
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
cpu_usage_t as 'CPU load % ', 
updated as 'DATE' 
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

ram_history_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
updated as 'DATE' 
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
disk_history_w = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
updated as 'Date'
FROM disk
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
net_history_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
        # graphs

cpu_usage_t_vs_time_w = """
SELECT cpu_usage_t, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

cpu_freq_vs_time_w = """
SELECT cur_freq, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

coretemp_vs_time_w = """
SELECT coretemp, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;"""

resvb_vs_time_w = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;"""

sentb_vs_time_w = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;"""

rio_vs_time_w = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;"""

wio_vs_time_w = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;"""

swap_vs_time_w = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

ram_vs_time_w = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
WHERE month(updated) = month(curdate()) AND
week(updated) = week(curdate())
ORDER BY updated
DESC LIMIT 10;
"""


# Monthly 

        # tables

cpu_history_m = """
SELECT ROUND(cur_freq) as 'CPU frequency - actual', 
cpu_usage_t as 'CPU load % ', 
updated as 'DATE' 
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

ram_history_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB',
ROUND(swap_used / 1024 / 1024, 2) as 'SWAP used in MB', 
updated as 'DATE' 
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
disk_history_m = """
SELECT ROUND(write_io / 1024 / 1024 / 1024, 2) as 'Write I/O in GB',
ROUND(read_io / 1024 / 1024 / 1024, 2) as 'Read I/O in GB',
ROUND(d_used / 1024 / 1024 / 1024, 2) as 'Disk used in GB',
updated as 'Date'
FROM disk
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
net_history_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB',
ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB',
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
        # graphs

cpu_usage_t_vs_time_m = """
SELECT cpu_usage_t, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

cpu_freq_vs_time_m = """
SELECT cur_freq, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

coretemp_vs_time_m = """
SELECT coretemp, DATE_FORMAT(updated, '%Y-%m-%d  %T') 
FROM cpu 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;"""

resvb_vs_time_m = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;"""

sentb_vs_time_m = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;"""

rio_vs_time_m = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;"""

wio_vs_time_m = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;"""

swap_vs_time_m = """
SELECT ROUND(swap_used / 1024 / 1024, 2) as 'Used SWAP in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""

ram_vs_time_m = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
WHERE year(updated) = year(curdate()) AND
month(updated) = month(curdate())
ORDER BY updated
DESC LIMIT 10;
"""
