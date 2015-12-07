from __future__ import print_function

import json
import signal
import logging
import traceback
import datetime as dt

from time import sleep
from os import getpid, environ
from contextlib import closing
from multiprocessing import Process, Value

from gsconn import order_writer
import config


logging.basicConfig(
    filename=config.LOGFILE,
    level=config.LOGLEVEL,
)


def parse_order(line):
    data = json.loads(line.decode('string_escape'))
    dish = data['dish']
    location = data['location']
    phone = int(data['phone'])
    return (dish, location, phone)


def populate_data(f):
    order_list = []
    while True:
        l = f.readline()
        if not l or len(l) == 0:
            break
        else:
            try:
                order = parse_order(l)
                order_list.append(order)
            except:
                logging.error(traceback.format_exc())
                continue
    return order_list


def main(file_log, loc_log, pid_log):
    SIG_MARK = Value('i', False)  # "Mutex-ish" global variable
    open(pid_log, 'w').write(str(getpid()))
    dump_order = order_writer()

    def worker(mark):
        try:
            position = int(open(loc_log).read())
        except:
            position = 0
        f = open(file_log)
        f.seek(position)
        while True:
            order_list = populate_data(f)
            error = dump_order(order_list)
            # error = print(order_list)
            if error:  # On error, rewind the file descriptor
                f.seek(position)
            else:      # Otherwise, proceed and update the log
                position = f.tell()
                open(loc_log, 'w').write(str(position))
            if mark.value:
                open(loc_log, 'w').write('0')
                return
            sleep(60)

    def sig_hand(signum, stack):
        SIG_MARK.value = True
        logging.info('>> SIG_MARK %d' % SIG_MARK.value)

    signal.signal(signal.SIGUSR1, sig_hand)
    p = Process(target=worker, args=(SIG_MARK,))
    p.start()


if __name__ == '__main__':
    pass

