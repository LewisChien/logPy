#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__= 'Allen'
'''
    获取跨服战玩家数据
'''
import os,sys,re,time
from utils.logutils import logError,logINFO
from db_utils.dbexec import DBExecUtil


sql_insert = "INSERT INTO `gm_cmd` (INSERTDATE, Cmd) VALUES (NOW(), %s)"
sql_server = "SELECT serverid FROM `cfg_open_server` WHERE state=1 AND isMerged=0 AND serverid=1067"
sql_log = "SELECT Cmd FROM gm_cmd_log WHERE Cmd LIKE 'custom_gift=%' AND INSERTDATE>'2015-06-10 12:10:23' ORDER BY INSERTDATE DESC LIMIT 10"
sql_user = "SELECT surpporter FROM bts_supportlog WHERE ROUND in (4,8) and reward=0"

#生成连接池名
def genPool(serverid):
	return 'dbgame_' + str(serverid)

#获取需要补偿的玩家
def getNeedUsr(poolname, dbexec):
	return dbexec.doSelect(poolname, sql_user)

'''
检查该服务器是否发送过奖励
@return True-需要发送奖励,False-已发过奖励
'''
def checkReward(poolname, dbexec):
	pattern = re.compile(r'1\+1\+1000')
	result = dbexec.doSelect(poolname, sql_log)

	if result == False:
		return True
	else:
		for row in result:
			rmatch = re.search(pattern, str(row['Cmd']))
			if rmatch:
				logINFO('--------poolname = ' + poolname + ' -- HAVE Send-------')
				return False
		return True

'''
获取服务器ID
'''
def getUsingServer(dbexec):
	return dbexec.doSelect('passport', sql_server)

'''
发送奖励
'''
def sendReward(dbexec):
	param = []
	count = 0
	#检查是否需要发送
	servers = getUsingServer(dbexec)
	if servers == False:
		pass
	else:
		for row in servers:
			poolname = genPool(row['serverid'])
			if checkReward(poolname, dbexec) == True:
				
				players = getNeedUsr(poolname, dbexec)
				if players == False:
					pass
				else:
					print u'需要发送奖励 ---- ' + poolname
					for role in players:
						reward = 'custom_gift=%d;1+1+1000;' % role['surpporter']
						logINFO(poolname + ' :: ' + reward)
						param.append(reward)
						count += 1
						if count % 200 == 0:
							dbexec.insert_many(poolname, sql_insert, param)
							count = 0
							param = []
							time.sleep(0.5)

					dbexec.insert_many(poolname, sql_insert, param)
			else:
				print u'pass ::::: poolname = ' + poolname
		
	

if __name__=='__main__':
	dbexec = DBExecUtil()
	sendReward(dbexec)