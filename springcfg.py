#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Allen'

import os, sys
from utils.excel import xlsxParse

file_path='E:/dumps/spring.txt'

def dynamicSource(serverid):
	return '				<entry value-ref="dbgame_%d" key="dbgame_%d"></entry>\n' % (serverid,serverid)


def db_game(serverid, ip):
	str = '	<bean id="dbgame_%d" parent="basicDataSource">\n' % serverid
	str += '		<property name="url">\n'
	str += '			<value>jdbc:mysql://%s:3306/db_game?autoReconnectForPools=true&amp;zeroDateTimeBehavior=convertToNull&amp;useUnicode=true&amp;characterEncoding=utf8</value>\n' % ip
	str += '		</property>\n'
	str += '	</bean>\n'
	return str

def genconfig(path, sheet):

	f = open(file_path, "w+")

	dict_data = xlsxParse(path, sheet)
	print dict_data

	str = '	<bean id="db_recharge" parent="basicDataSource">\n'
	str += '		<property name="url">\n'
	str += '			<value>jdbc:mysql://10.254.243.33:3306/xh_member?autoReconnectForPools=true&amp;zeroDateTimeBehavior=convertToNull&amp;useUnicode=true&amp;characterEncoding=utf8</value>\n'
	str += '		</property>\n'
	str += '	</bean>\n'
	str_choose = '	<bean id="dataSource" class="com.utgame.db.DynamicDataSource">\n'
	str_choose += '		<property name="targetDataSources">\n'
	str_choose += '			<map key-type="java.lang.String">\n'
	str_choose += '				<entry value-ref="db_recharge" key="db_recharge"></entry>\n'
	if dict_data:
		for k,v in dict_data.iteritems():
			serverid = v[4]
			ip = v[2]
			str += db_game(serverid, ip)
			str_choose += dynamicSource(serverid)

		str = str+str_choose
		str += '			</map>\n'
		str += '		</property>\n'
		str += '		<property name="defaultTargetDataSource" ref="db_recharge" />\n'
		str += '	</bean>\n'

		f.write(str)

	if f:
		f.close()
	print 'over'

if __name__ == '__main__':
	genconfig('E:/dumps/xh_20150813.xlsx', u'安卓DB')