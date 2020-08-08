import time
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
import mysql.connector
from visualizer import GetSQLData

def cpu_load_by_time():
    cpu = []
    time = []
    q = "SELECT cpu_usage_t, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM cpu ORDER BY updated DESC LIMIT 15;"
    get_q = GetSQLData(q)
    result = get_q.GetData()
    for item in result:
            cpu.append(item[0])
            time.append(item[1])
    dates = [dateutil.parser.parse(s) for s in time]
    plt.subplots_adjust(bottom=0.3)
    plt.xticks( rotation=50 )
    plt.title('CPU load ordered by time')
    ax=plt.gca()
    ax.set_xticks(dates)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,cpu)
    plt.savefig('static/cpu_load_by_time.png')
    return plt.clf()

def cpu_freq_by_time():
    cpu = []
    time = []
    q = "SELECT cur_freq, DATE_FORMAT(updated, '%Y-%m-%d  %T') FROM cpu ORDER BY updated DESC LIMIT 15;"
    get_q = GetSQLData(q)
    result = get_q.GetData()
    for item in result:
            cpu.append(item[0])
            time.append(item[1])
    dates = [dateutil.parser.parse(s) for s in time]
    plt.subplots_adjust(bottom=0.3)
    plt.xticks( rotation=50 )
    plt.title('CPU frequency ordered by time')
    ax=plt.gca()
    ax.set_xticks(dates)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,cpu)
    plt.savefig('static/cpu_freq_by_time.png')
    return plt.clf()

def cpu_f_vs_cpu_l():
    q = "SELECT cur_freq,cpu_usage_t FROM cpu ORDER BY cpu_usage_t DESC LIMIT 15;"
    get_q = GetSQLData(q)
    result = get_q.GetData()
    freq = []
    cpu = []
    for item in result:
        freq.append(item[0])
        cpu.append(item[1])
    plt.subplots_adjust(bottom=0.2)
    plt.title('CPU frequency VS CPU load')
    plt.xticks(rotation=45)
    plt.bar(cpu,freq)
    plt.savefig('static/cpuf_vs_cpul.png')
    return plt.clf()



def ParamVsTime(q, name):
    param = []
    time = []
    get_q = GetSQLData(q)
    result = get_q.GetData()
    for item in result:
            param.append(item[0])
            time.append(item[1])
    dates = [dateutil.parser.parse(s) for s in time]
    plt.subplots_adjust(bottom=0.3)
    plt.xticks( rotation=50 )
    plt.title(name)
    ax=plt.gca()
    ax.set_xticks(dates)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,param)
    plt.savefig('static/{}.png'.format(name))
    return plt.clf()

q1 = "SELECT ROUND(used_mem / 1024 / 1024, 2) as 'Used RAM in MB', DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' from ram ORDER by updated DESC LIMIT 20;"
q2 = "SELECT ROUND(write_io / 1024 / 1024, 2) as 'Write I/O in MB', DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' from disk ORDER by updated DESC LIMIT 20;"
q3 = "SELECT ROUND(read_io / 1024 / 1024, 2) as 'Read I/O in MB', DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' from disk ORDER by updated DESC LIMIT 20;"
q4 = "SELECT ROUND(sent_b / 1024 / 1024, 2) as 'Sent over network in MB', DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' from network ORDER by updated DESC LIMIT 20;"
q5 = "SELECT ROUND(recv_b / 1024 / 1024, 2) as 'Received over network in MB', DATE_FORMAT(updated, '%Y-%m-%d  %T') as 'DATE' from network ORDER by updated DESC LIMIT 20;"
t1 = 'RAM_vs_Time'
t2 = 'Write_IO'
t3 = 'Read_IO'
t4 = 'Sent_MB'
t5 = 'Received_MB'