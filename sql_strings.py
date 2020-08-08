############################
#
#   SQL views for the UI interfase
#
#   Note: edit carefully due to graph and dashboard representing
#
#
#############################
############
#
#   SQL Queries for charts/pies (dynamic system information)
#
############
cpu_q = """
SELECT ROUND(c.cur_freq)as Current_frequency_MHz, 
ROUND(s.max_freq) as MAX_frequency_MHz 
FROM cpu c, sysinfo s 
ORDER BY c.updated 
DESC LIMIT 1;"""
cpu_l = 'Current','MAX'
cpu_t = 'CPU_frequency'
net_p_q = """
SELECT CONCAT(sent_p) Sent_packets, 
CONCAT(recv_p) Received_packets 
FROM network 
ORDER by updated 
DESC LIMIT 1;"""
net_p_l = 'Sent packets', 'Received packets'
net_p_t = 'Network_packets'
net_mb_q = """
SELECT CONCAT(ROUND(sent_b / 1024 / 1024 )) Sent_MB, 
CONCAT(ROUND(recv_b / 1024 / 1024 )) Received_MB 
FROM network 
ORDER by updated 
DESC LIMIT 1;"""
net_mb_l = 'Sent MB', 'Received MB'
net_mb_t = 'Network_MB'
ram_q = """
SELECT CONCAT(ROUND(s.total_mem / 1024 / 1024 / 1024)) Total_RAM, 
CONCAT(ROUND(r.avail_mem / 1024 / 1024 / 1024)) Available_RAM, 
CONCAT(ROUND(r.used_mem / 1024 / 1024 / 1024)) Used_RAM  
FROM sysinfo s, ram r 
ORDER by r.updated 
DESC LIMIT 1;"""
ram_l = 'Total', 'Available', 'Used'
ram_t = 'RAM'
disk_q = """
SELECT CONCAT(ROUND(s.d_total / 1024 / 1024 / 1024)) Total, 
CONCAT(ROUND(d.d_used / 1024 / 1024 / 1024)) Used, 
CONCAT(ROUND(d.d_free / 1024 / 1024 / 1024)) Free 
FROM sysinfo s, disk d 
ORDER by d.updated 
DESC LIMIT 1;"""
disk_l = 'Total', 'Used', 'Available'
disk_t = 'Disk'
swap_q = """
SELECT CONCAT(ROUND(s.swap_total / 1024 / 1024 / 1024)) Total_SWAP, 
CONCAT(ROUND(r.swap_free / 1024 / 1024 / 1024)) Available_SWAP, 
CONCAT(ROUND(r.swap_used / 1024 / 1024 / 1024)) Used_SWAP  
FROM sysinfo s, ram r 
ORDER by r.updated 
DESC LIMIT 1;"""
swap_l = 'Total', 'Available', 'Used'
swap_t = 'Swap'
#############
#
#   SQL Queries for tables/cells/headers (static system information)
#
#############
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
SELECT nodename, osname, osarch, cpuarch, boot 
FROM sysinfo 
ORDER BY updated DESC LIMIT 1;"""
sysinfo_q2 = """
SELECT CONCAT(ROUND(d_total / 1024 / 1024 / 1024)) as total_space, 
CONCAT(ROUND(total_mem / 1024 / 1024 / 1024)) as total_ram, 
CONCAT(ROUND(swap_total / 1024 / 1024 / 1024)) as total_swap, cores_ph, cores_t, max_freq, min_freq 
FROM sysinfo 
ORDER BY updated DESC LIMIT 1;"""
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
SELECT ROUND(write_io / 1024 /1024, 2) as 'Write I/O in MB',
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

ram_vs_time_q = """
SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM ram 
ORDER by updated 
DESC LIMIT 20;
"""
ram_vs_time_t = 'ram_vs_time'


wio_vs_time_q = """
SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
ORDER by updated 
DESC LIMIT 20;"""
wio_vs_time_t = 'wio_ws_time'


rio_vs_time_q = """
SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM disk 
ORDER by updated DESC LIMIT 20;"""
rio_vs_time_t = 'Read_IO'

sentb_vs_time_q = """
SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 20;"""
sentb_vs_time_t = 'Sent_MB'

resvb_vs_time_q = """
SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', 
DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' 
FROM network 
ORDER by updated DESC LIMIT 20;"""
resvb_vs_time_t = 'Received_MB'