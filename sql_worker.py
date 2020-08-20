import time
import sys
from datetime import datetime
import mysql.connector
import logging
from system_data import *
from sql_strings import *

FORMAT = '%(asctime)-15s    %(message)s \n'
logging.basicConfig(filename="application.log", level=logging.DEBUG, format=FORMAT)

def insert_data(query, params=()):
    """
    Function accepting sql query from sql_stings.py and parameters to insert from system_data.py

    Example: 
    
    insert_data(your_sql_query, (param_1, param_2, param_x))
    """
    try:
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        cursor.execute(query, (params))
        mydb.commit()
        cursor.close()
        mydb.close()
        logging.info('Jarvis INFO: sql_worker.insert_data()')
        logging.info(f'Jarvis INFO: SQL: [{query}]')
    except Exception as e:
        logging.error(f'JARVIS: Caught exception in sql_worker.insert_data() [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)

def main():
    """
    Function for endless data insert. Starting with webserver and can be stopped
    either simulataneously with it via startap application (jarvis.sh / jarvis.bat)
    or manually from CMD / Task Manager (Linux / Windos)
    """
    while True:
        try:
            logging.info('Jarvis INFO: sql_worker.main() woke up!')
            insert_data(ram_insert, (avail_mem, used_mem, swap_used, swap_free))
            insert_data(cpu_insert, (cur_freq, cpu_usage_t, coretemp))
            insert_data(disk_insert, (read_io, write_io, d_used, d_free))
            insert_data(net_insert, (sent_b, sent_p, recv_b, recv_p))
            insert_data(info_insert, (osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total, boot_h))
            logging.info('Jarvis INFO: sql_worker.main() sleep.')
            time.sleep(300)
        except Exception as e:
            logging.error(f'JARVIS: Caught exception in sql_worker.main() [ {e} ]')
            logging.error('JARVIS: Full trace: \n', exc_info=1)

if __name__ == '__main__':
    try:            
        main()
    except Exception as e:
        logging.error(f'JARVIS: Caught exception [ {e} ]')
        logging.error('JARVIS: Full trace: \n', exc_info=1)