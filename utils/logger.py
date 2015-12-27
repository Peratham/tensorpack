#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: logger.py
# Author: Yuxin Wu <ppwwyyxx@gmail.com>

import logging
import os
from termcolor import colored

__all__ = []

class MyFormatter(logging.Formatter):
    def format(self, record):
        date = colored('[%(asctime)s %(lineno)d@%(filename)s:%(name)s]', 'green')
        msg = '%(message)s'
        if record.levelno == logging.WARNING:
            fmt = date + ' ' + colored('WRN', 'red', attrs=['blink']) + ' ' + msg
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            fmt = date + ' ' + colored('ERR', 'red', attrs=['blink', 'underline']) + ' ' + msg
        else:
            fmt = date + ' ' + msg
        self._fmt = fmt
        return super(MyFormatter, self).format(record)

def getlogger():
    logger = logging.getLogger('tensorpack')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(MyFormatter(datefmt='%d %H:%M:%S'))
    logger.addHandler(handler)
    return logger

logger = getlogger()

for func in ['info', 'warning', 'error', 'critical', 'warn']:
    locals()[func] = getattr(logger, func)

def set_file(path):
    if os.path.isfile(path):
        warn("File \"{}\" exists! backup? (y/n)".format(path))
        resp = raw_input()
        if resp in ['y', 'Y']:
            from datetime import datetime
            backup_name = path + datetime.now().strftime('.%d-%H%M%S')
            import shutil
            shutil.move(path, backup_name)
            info("Log '{}' moved to '{}'".format(path, backup_name))
    hdl = logging.FileHandler(
        filename=path, encoding='utf-8', mode='w')
    logger.addHandler(hdl)