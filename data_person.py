#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from utils.logutils import logError,logINFO
from utils.excel import data_of_excel
from db_utils.dbexec import DBExecUtil

#获取当前文件夹的绝对路径
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'logs/result.csv')

def player_uid():
	dbexec = DBExecUtil()
	list = data_of_excel('E:/dumps/1.xls', 'Sheet1', 3)
	sql = None
	try:
		f = open(file_path, "w+")
		try:
			for x in range(0, len(list)):
				rlist = list[x]
				
				if str(rlist[1]).find('.0') == -1:
					sql= "SELECT PlatformUID,ID,ServerIndex FROM player WHERE NAME= '%s'" % rlist[0]
				else:
					sql = "SELECT PlatformUID,ID,ServerIndex FROM player WHERE PlatformUID= '%s'" % str(rlist[1]).replace('.0', '')
				
				result = dbexec.doSelect('dbgame_' + str(rlist[2]).replace('.0', ''), sql)
				if result == False:
					pass
				else:
					for row in result:
						line = "%s	%s	%s" % (str(row['PlatformUID']), str(row['ID']), str(row['ServerIndex'])) + "\n"
						print line
						f.write(line)
		finally:
			f.close()
	except Exception, e:
		logError('角色UID', e)
	print 'finish'
	
if __name__ == '__main__':
	player_uid()