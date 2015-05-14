#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from xml.dom import minidom
#获取当前文件夹的绝对路径
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'db_conf.xml')

def xmlUtil():
	
	db_dict = {}
	
	#使用minidom解析器打开 XML 文档
	dom = minidom.parse(file_path)
	#获取根节点
	root = dom.firstChild
	#获取子节点
	nodes = root.childNodes
	for node in nodes:
		if node.nodeType == node.TEXT_NODE:
			pass
		else:
			arrtuple = None
			pool = node.getAttribute('pool')
			db_url = node.getAttribute('db_url')
			db_port = node.getAttribute('db_port')
			db_name = node.getAttribute('db_name')
			db_usr = node.getAttribute('db_usr')
			db_pass = node.getAttribute('db_pass')
			arrtuple = (db_url,db_port,db_name,db_usr,db_pass)
			db_dict[pool] = arrtuple
	
	return db_dict