import psutil
import platform
import time
import sys
from datetime import datetime
import mysql.connector
import logging
import subprocess
from subprocess import Popen, PIPE

dbconfig = {
        'host':     '127.0.0.1',
        'user':     'root',
        'password':  'root',
        'database': 'pyguard_v1',
        }
mydb = mysql.connector.connect(pool_name = "pyguard_v1",
                                       pool_size = 20,
                                       **dbconfig)
cursor = mydb.cursor()
FORMAT = '%(asctime)-15s    %(message)s \n'
logging.basicConfig(filename="application.log", level=logging.DEBUG, format=FORMAT)

def insert_ram():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    swap_used = swap.used
    swap_free = swap.free
    avail_mem = svmem.available
    used_mem = svmem.used
    q = "INSERT INTO ram (avail_mem, used_mem, swap_used, swap_free) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(q, (avail_mem, used_mem, swap_used, swap_free))
        mydb.commit()
        logging.info('MySQL inserted OK. \n SQL: [{}]'.format(q))
    except Exception and NameError and TypeError and ValueError and SyntaxError:
        logging.error('MySQL failed to perform \n SQL: [{}]. Traceback:'.format(q), exc_info=True)

def insert_cpu():
    cpufreq = psutil.cpu_freq()
    cur_freq = cpufreq.current
    cpu_usage_t = psutil.cpu_percent()
    q = "INSERT INTO cpu (cur_freq, cpu_usage_t) VALUES (%s, %s)"
    try:
        cursor.execute(q, (cur_freq, cpu_usage_t))
        mydb.commit()
        logging.info('MySQL inserted OK \n SQL: [{}]'.format(q))
    except Exception and NameError and TypeError and ValueError and SyntaxError:
        logging.error('MySQL failed to perform \n SQL: [{}]. Traceback:'.format(q), exc_info=True)
    

def insert_disk():
    d = psutil.disk_usage('/')
    d_used = d.used
    d_free = d.free
    disk_io = psutil.disk_io_counters()
    read_io = disk_io.read_bytes
    write_io = disk_io.write_bytes
    q = "INSERT INTO disk (read_io, write_io, d_used, d_free) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(q, (read_io, write_io, d_used, d_free))
        mydb.commit()
        logging.info('MySQL inserted OK \n SQL: [{}]'.format(q))
    except Exception and NameError and TypeError and ValueError and SyntaxError:
        logging.error('MySQL failed to perform \n SQL: [{}]. Traceback:'.format(q), exc_info=True)
    

def insert_network():
    net_io = psutil.net_io_counters()
    sent_b = net_io.bytes_sent
    sent_p = net_io.packets_sent
    recv_b = net_io.bytes_recv
    recv_p = net_io.packets_recv
    q = "INSERT INTO network (sent_b, sent_p, recv_b, recv_p) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(q, (sent_b, sent_p, recv_b, recv_p))
        mydb.commit()
        logging.info('MySQL inserted OK \n SQL: [{}]'.format(q))
    except Exception and NameError and TypeError and ValueError and SyntaxError:
        logging.error('MySQL failed to perform \n SQL: [{}]. Traceback:'.format(q), exc_info=True)

def insert_info():
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
    q = "INSERT INTO sysinfo (osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total, boot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(q, (osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total, boot_h))
        mydb.commit()
        logging.info('MySQL inserted OK \n SQL: [{}]'.format(q))
    except Exception and NameError and TypeError and ValueError and SyntaxError:
        logging.error('MySQL failed to perform \n SQL: [{}]. Traceback:'.format(q), exc_info=True)
    


def insert_all():
    insert_info()
    insert_cpu()
    insert_disk()
    insert_network()
    insert_ram()

def main():
    while True:
        insert_all()
        logging.info('Sleep time. Next insert in 30 s')
        time.sleep(30)

try:
    logging.info('Inserting data - START')
    p1 = subprocess.Popen('python3 jarvis.py', stderr=PIPE, stdout=PIPE, shell=True)
    main()
    mydb.close()
    logging.info('Inserting data - STOP')
except Exception as e:
    logging.error("Error occured while inserting data. Traceback: {}".format(e))