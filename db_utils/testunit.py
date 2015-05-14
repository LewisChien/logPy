#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import unittest
import dbpool
sys.path.append('..')
from utils.logutils import *

logINFO(' 单元测试类 ------ Start')

class DBTestUnit(unittest.TestCase):
	
	#初始化
	def setUp(self):
		self.dbclass = dbpool.DBUtilPool()
	
	'''
	退出清理工作
	'''
	def tearDown(self):
		pass

	#具体测试用例
	def testBuildPool(self):
		self.assertEqual(self.dbclass.buildPool())

	if __name__ == "__main__":
		unittest.main()