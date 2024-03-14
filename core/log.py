"""  
@Time: 2024/3/14 14:52 
@Auth: Y5neKO
@File: log.py 
@IDE: PyCharm 
"""
import logging
import os
import traceback
import time


def log_error(exception):
    if not os.path.exists('./log/'):
        os.mkdir('./log')
    log_file_name = time.strftime("%Y_%m_%d", time.localtime())
    logging.basicConfig(filename='./log/' + log_file_name + '.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error("An exception occurred:", exc_info=exception)
    logging.error(traceback.format_exc())
