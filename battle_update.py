#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Allen'

'''
跨服战奖励补发
1,根据gm_cmd_log生成中间表，获取玩家发送奖励次数，生成中间表temp_gm_log
2,获取跨服战奖励LOG，获取玩家应发奖励次数，匹配中间表temp_gm_log
3,根据匹配，发送未给的奖励
'''

import os,sys,re,time
from utils.logutils import logError,logINFO
from db_utils.dbexec import DBExecUtil

txtpath = "mjp.txt"

#Insert into GM_CMD
sql_insert = "INSERT INTO `gm_cmd` (INSERTDATE, Cmd) VALUES (NOW(), %s)"
#16进8压中角色ID
sql_query = "SELECT DISTINCT surpporter FROM `bts_supportlog` WHERE plyid=%s AND ROUND=16"

#生成DBGAME连接池名
def poolCreate(serverid):
	return 'dbgame_' + str(serverid)
	
#查询方法
def query(poolname, sql, dbexec):
	return dbexec.doSelect(poolname, sql)


#读取txt文件
def readtxt():
	dline = {}
	f = open(txtpath, "r")
	for line in f:
		if line:
			key,value = line.split(',')
			dline[key] = value.strip()
	f.close()
	return dline

#处理奖励发送
def send(dbexec=None):
	count = 0
	param = []
	dic_line = readtxt()
	try:
		if dic_line:
			for k,v in dic_line.iteritems():
				poolname = poolCreate(v)
				sql = sql_query % str(k)
				
				players = query(poolname, sql, dbexec)
				if players == False or players == None:
					pass
				else:
					for row in players:
						reward = 'custom_gift=%d;1+1+200;' % row['surpporter']
						logINFO(poolname + ' :: ' + reward)
						param.append(reward)
						count += 1
						if count >= 200:
							dbexec.insert_many(poolname, sql_insert, param)
							count = 0
							param = []
							time.sleep(0.5)

					dbexec.insert_many(poolname, sql_insert, param)
					count = 0
					param = []
					print 'finish :: ' + str(poolname) + '; ' + str(k)
					
	except Exception, e:
		print e


if __name__ == '__main__':
	dbexec = DBExecUtil()
	send(dbexec)
	print 'over'