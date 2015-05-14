#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, os
import logging.config

BASE_DIR = os.path.dirname(__file__)
log_path = os.path.join(BASE_DIR, os.pardir + '/conf/logging.conf')

logging.config.fileConfig(log_path);
logger = logging.getLogger('A1')
logger2 = logging.getLogger('A2')

def logError(msg, e):
	logger2.error(msg)
	logger2.error(e)
	
def logINFO(msg):
	logger.info(msg)