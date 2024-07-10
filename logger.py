import logging
import traceback
import sys

file_log = logging.FileHandler('logs/logs.log')
file_log.setLevel(logging.WARNING)

console_out = logging.StreamHandler()
console_out.setLevel(logging.INFO)

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s | %(threadName)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.DEBUG)

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    logging.error(text)

sys.excepthook = log_uncaught_exceptions