#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import MySQLdb

from utils.logutils import *
from conf.db_conf import *

db_dict = xmlUtil()

def createConn(poolname):
	arr = db_dict[poolname]
	host=arr[0]
	port=int(arr[1])
	user=arr[3]
	passwd=arr[4]
	db=arr[2]
	
	conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
	return conn
	
	
	