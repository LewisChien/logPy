#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

sys.path.append('..')
from utils.logutils import *
from conf.db_conf import *

'''
数据库连接池公用类
'''
class DBUtilPool(object):
	
	@staticmethod
	def buildPool():
		pool_dict = {}
		db_dict = xmlUtil()
		try:
			for db_key in db_dict.keys():
				arr = db_dict[db_key]
				pool = PooledDB(creator=MySQLdb, mincached=1,maxcached=20,
							host=arr[0],port=int(arr[1]),user=arr[3],passwd=arr[4],db=arr[2],
							use_unicode=False,charset='utf8',cursorclass=DictCursor)
				
				pool_dict[db_key] = pool
		except Exception, e:
			logError('初始化连接池Error', e)
		return pool_dict

	'''
	创建单个连接池
	'''
	@staticmethod
	def buildSinglePool(poolname):
		db_dict = xmlUtil()		#获取xml配置
		pool = None
		try:
			#数据字典获取连接池信息
			arr = db_dict[poolname]
			pool = PooledDB(creator=MySQLdb, mincached=1,maxcached=20,
						host=arr[0],port=int(arr[1]),user=arr[3],passwd=arr[4],db=arr[2],
						use_unicode=False,charset='utf8',cursorclass=DictCursor)
		except Exception, e:
			logError('重置连接池失败', e)
		return pool
	
	'''
	根据连接池名称获取Pool
	'''
	@staticmethod
	def getPoolbyName(poolname):
		pool_dict = DBUtilPool.buildPool()
		return pool_dict[poolname]
	
	'''
	根据连接池名称获取连接
	'''
	@staticmethod
	def getConn(poolname):
		pool = None
		try:
			pool = DBUtilPool.getPoolbyName(poolname)
		except Exception, e:
			logError('获取数据连接池Error', e)
		return pool.connection()
	
	'''
	判断连接池是否存在
	@return False is None,True is NotNull
	'''
	@staticmethod
	def boolExist(poolname):
		pool_dict = DBUtilPool.buildPool()
		print pool_dict[poolname]
		if pool_dict[poolname] is None:
			print 'false'
			return False
		else:
			print 'true'
			return True

	'''
	私有方法,获取当前连接最后一次插入操作生成的id
	'''
	def __getInsertId(poolname):
		cursor = DBUtilPool.getCursor(poolname)
		cursor.execute("SELECT @@IDENTITY AS id")
		result = cursor.fetchall()
		return result[0]['id']
	
if __name__ == '__main__':
	DBUtilPool.getConn('db_game')
