import time
from time import time
import sys
import mysql.connector
import logging
from system_data_kpi import *
from sql_strings import *
from visual_worker import performance
##########################
#
#   LOGGING PROPERTIES
#
##########################
FORMAT = '%(asctime)s  %(levelname)s :  %(message)s'
logging.basicConfig(filename="application.log", level=logging.INFO, format=FORMAT)

@performance
def insert_data(query, params=()):
    """
    Function accepting sql query from sql_stings.py and parameters to INSERT from system_data.py

    Example: 
    
    insert_data(your_sql_query, (param_1, param_2, param_x))
    """
    try:
        mydb = mysql.connector.connect(**dbconfig)
        cursor = mydb.cursor()
        cursor.execute(query, (params))
        mydb.commit()
        logging.info('JARVIS INFO: sql_worker() -> insert_data() \n')
        logging.info(f'JARVIS INFO: insert_data() query used: {query} \n')
    except Exception as e:
        logging.error(f'JARVIS: Caught exception in sql_worker() -> insert_data() [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
        mydb.close()
        cursor.close()
    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    while True:
        try:
            logging.info('JARVIS INFO: sql_worker -> call system_data() \n')
            logging.info('JARVIS INFO: system_data_kpi -> KPI cache refresh START \n')
            osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total = get_sys()
            avail_mem, used_mem, swap_used, swap_free = get_ram()
            cur_freq, cpu_percent, coretemp, boot_h, loadavg = get_cpu()
            read_io, write_io, d_used, d_free = get_disk()
            sent_b, sent_p, recv_b, recv_p = get_net()
            logging.info('JARVIS INFO: system_data_kpi -> KPI cache refresh END \n')
        except Exception as e:
            logging.error('JARVIS ERROR: sql_worker -> FAILED call system_data() \n')
            logging.error('JARVIS ERROR: system_data -> KPI cache refresh FAILED \n')
            logging.error(f'JARVIS: Caught exception:  {e}  \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)

        try:
            logging.info('JARVIS INFO: sql_worker -> main() Begin DB update \n')
            insert_data(info_insert, (osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total))
            insert_data(ram_insert, (avail_mem, used_mem, swap_used, swap_free))
            insert_data(cpu_insert, (cur_freq, cpu_percent, coretemp, boot_h, loadavg))
            insert_data(disk_insert, (read_io, write_io, d_used, d_free))
            insert_data(net_insert, (sent_b, sent_p, recv_b, recv_p))
            logging.info('JARVIS INFO: sql_worker -> main() End DB update \n')
            time.sleep(60)
        except Exception as e:
            logging.error('JARVIS INFO: sql_worker -> main() DB update failed! \n')
            logging.error(f'JARVIS: Caught exception:  {e}  \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)
            time.sleep(60)