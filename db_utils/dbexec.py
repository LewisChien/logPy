#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import MySQLdb
from dbpool import DBUtilPool

sys.path.append('..')
from utils.logutils import *

'''
数据库执行公用类
'''
class DBExecUtil(object):
	
	'''
	获取数据库连接
	'''
	def getConnectByPool(self, poolname):
		conn = None;
		try:
			pool = DBUtilPool.getPoolbyName(poolname)
			if pool is not None:
				conn = pool.connection()
			elif conn is None:
				pool = DBUtilPool.buildSinglePool(poolname)
				conn = pool.connection()
		except Exception, e:
			logError('根据连接池获取连接Error', e)
		return conn
	
	'''
	查询结果集
	'''
	def doSelect(self, poolname, sql, param=None):
		result = None
		cursor = None
		conn = None
		try:
			try:
				conn = self.getConnectByPool(poolname)
				cursor = conn.cursor()
				if param is None:
					count = cursor.execute(sql)
				else:
					count = cursor.execute(sql, param)
				
				if count>0:
					result = cursor.fetchall()
				else:
					result = False
				
				conn.commit()
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()
		except Exception, e:
			logError('查询结果集Error', e)
		return result
		
	'''
	INSERT 单条记录
	@param value 要插入的记录数据tuple/list
	@return insertId 受影响的行数
	'''
	def insert_one(self, poolname, sql, value=None):
		cursor = None
		conn = None
		count = None
		bool = None
		try:
			try:
				conn = self.getConnectByPool(poolname)
				cursor = conn.cursor()
				#执行sql语句
				if value is None:
					count = cursor.execute(sql)
				else:
					count = cursor.execute(sql, value)
				conn.commit()
				
				if count == 1:
					bool = True
				else:
					bool = False
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()
		except Exception, e:
			if conn is not None:
				conn.rollback()
			logError('插入一条记录Error', e)
		return bool
		
	'''
	INSERT 多条记录
	@param value 要插入的记录数据tuple/list[]
	@return count 受影响的行数
	'''
	def insert_many(self, poolname, sql, values):
		cursor = None
		conn = None
		count = None
		try:
			try:
				conn = self.getConnectByPool(poolname)
				cursor = conn.cursor()
				#执行sql语句
				count = cursor.executemany(sql, values)
				conn.commit()
				
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()
		except Exception, e:
			if conn is not None:
				conn.rollback()
			logError('插入多条记录Error', e)
		return count
	
	'''
	UPDATE
	@return 影响条数
	'''
	def update(self, poolname, sql, param=None):
		return self.__query(poolname, sql, param)
	
	'''
	DELETE
	@return 影响条数
	'''
	def delete(self, poolname, sql, param=None):
		return self.__query(poolname, sql, param)
	
	#私有方法
	def __query(self, poolname, sql, param=None):
		cursor = None
		conn = None
		count = None
		try:
			try:
				conn = self.getConnectByPool(poolname)
				cursor = conn.cursor()
				if param is None:
					count = cursor.execute(sql)
				else:
					count = cursor.execute(sql, param)
				conn.commit()
				
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()
		except Exception, e:
			if conn is not None:
				conn.rollback()
			logError('__query私有方法Error', e)
		return count
	
	def tableFunc(self, poolname, sql):
		cursor = None
		conn = None
		try:
			try:
				conn = self.getConnectByPool(poolname)
				cursor = conn.cursor()
				cursor.execute(sql)
				#conn.commit()
				
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()
		except Exception, e:
			if conn is not None:
				conn.rollback()
			logError('__query私有方法Error', e)
	
if __name__ == '__main__':
	dbexec = DBExecUtil()
	sql2 = "DROP TABLE IF EXISTS `temp_gm_log`"
	sql = '''CREATE TABLE `temp_gm_log` (
			`Cmd` VARCHAR(64) DEFAULT NULL COMMENT 'gm命令',
			`count` INT(10) DEFAULT NULL COMMENT '数量'
			) ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT='gm_cmd_log_temp';'''
	#sql = "update server_permit  set address=%s WHERE channel= %s"
	sql1 = "CREATE TABLE temp_gm_log LIKE gm_cmd_log"
	result = dbexec.insert_one('passport', sql)
