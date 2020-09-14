import time
from time import time
import sys
import mysql.connector
import logging
from system_data_kpi import *
from data_models import *
from visualize_data import performance
####################################################
#
#   Logging properties
#
####################################################
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
        logging.info('JARVIS: sql_worker() -> insert_data() \n')
    except Exception as e:
        logging.error(f'JARVIS: Caught exception in sql_worker() -> insert_data() [ {e} ] \n')
        logging.error('JARVIS: Full trace: \n', exc_info=1)
        logging.error(f'JARVIS: insert_data() query used: {query} \n')
        mydb.rollback()
        mydb.close()
        cursor.close()
    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    while True:
        try:
            logging.info('JARVIS: sql_worker -> system_data_kpi() \n')
            logging.info('JARVIS: system_data_kpi -> KPI cache refresh START \n')
            osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total = get_sys()
            avail_mem, used_mem, swap_used, swap_free = get_ram()
            cur_freq, cpu_percent, coretemp, boot_h, loadavg = get_cpu()
            read_io, write_io, d_used, d_free = get_disk()
            sent_b, sent_p, recv_b, recv_p = get_net()            
        except Exception as e:
            logging.error('JARVIS: sql_worker -> FAILED call system_data() \n')
            logging.error('JARVIS: system_data -> KPI cache refresh FAILED \n')
            logging.error(f'JARVIS: Caught exception:  {e}  \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)
        finally:
            logging.info('JARVIS: system_data_kpi -> KPI cache refresh END \n')

        try:
            logging.info('JARVIS: sql_worker -> main() Begin DB update \n')
            insert_data(info_insert, (osname, nodename, version, osarch, cpuarch, cores_ph, cores_t, max_freq, min_freq, total_mem, swap_total, d_total))
            insert_data(ram_insert, (avail_mem, used_mem, swap_used, swap_free))
            insert_data(cpu_insert, (cur_freq, cpu_percent, coretemp, boot_h, loadavg))
            insert_data(disk_insert, (read_io, write_io, d_used, d_free))
            insert_data(net_insert, (sent_b, sent_p, recv_b, recv_p))            
        except Exception as e:
            logging.error('JARVIS: sql_worker -> main() DB update failed! \n')
            logging.error(f'JARVIS: Caught exception:  {e}  \n')
            logging.error('JARVIS: Full trace: \n', exc_info=1)
            time.sleep(300)
        finally:
            time.sleep(300)
            logging.info('JARVIS: sql_worker -> main() End DB update \n')