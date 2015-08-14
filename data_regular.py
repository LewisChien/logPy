#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from utils.logutils import logError,logINFO
from db_utils.dbexec import DBExecUtil

#获取当前文件夹的绝对路径
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'logs/result.csv')

#获取腾讯所有服务器ID
def getUsingServer(dbexec):
	sql = "SELECT serverid FROM `cfg_open_server` WHERE serverId<1064 AND isMerged=0"
	return dbexec.doSelect('passport', sql)

def rechargeINFO_TX():
	dbexec = DBExecUtil()
	try:
		f = open(file_path, "w+")
		try:
			sql = """
				SELECT PlayerID,ServerIndex,SUM(good_price) as price FROM `log_recharge` 
				WHERE ServerTime>'2015-04-16 10:00:00' AND ServerTime<'2015-04-16 12:00:00' GROUP BY PlayerID
				"""
			servers = getUsingServer(dbexec)
			if servers == False:
				pass
			else:
				for row in servers:
					serverid = row['serverid']
					poolname = str(serverid) + "_log"
					result =  dbexec.doSelect(poolname, sql)
					for row in result:
						line = "%s	%s	%s" % (str(row['PlayerID']), str(row['ServerIndex']), str(row['price'])) + "\n"
						f.write(line)
					print poolname + " __over"
		finally:
			f.close()
	except Exception, e:
		logError('获取充值信息报错', e)
	print 'over'
	

if __name__ == '__main__':
	rechargeINFO_TX()
