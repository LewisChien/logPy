#!/usr/bin/python
#-*- coding:utf-8 -*- 

###20150205 入库

import multiprocessing,time,logging,sys,os,re,socket,commands,shutil

###定义日志函数
def write_exec_log(log_level,log_message):
	###创建一个logger
	logger = logging.getLogger('mysql_data.logger')
	logger.setLevel(logging.DEBUG)

	###建立日志目录
        log_dir  = "/tmp/"
        log_file = "dzz_mysql_data.log"
	if not os.path.isdir(log_dir):
		os.makedirs(log_dir,mode=0777)

	###创建一个handler用于写入日志文件
	fh = logging.FileHandler(log_dir + log_file)
	fh.setLevel(logging.DEBUG)

	###创建一个handler用于输出到终端
	th = logging.StreamHandler()
	th.setLevel(logging.DEBUG)

	###定义handler的输出格式
	formatter =logging.Formatter('%(asctime)s  %(name)s  %(levelname)s  %(message)s')
	fh.setFormatter(formatter)
	th.setFormatter(formatter)

	###给logger添加handler
	logger.addHandler(fh)
	logger.addHandler(th)

	###记录日志
	level_dic = {'debug':logger.debug,'info':logger.info,'warning':logger.warning,'error':logger.error,'critical':logger.critical}
	level_dic[log_level](log_message)

	###删除重复记录
	fh.flush()
	logger.removeHandler(fh)

	th.flush()
	logger.removeHandler(th)

###脚本排它锁函数
def script_exclusive_lock():
	pid_file  = '/tmp/dzz_mysql_data.pid'
	lockcount = 0
	while True:
		if os.path.isfile(pid_file):
			###打开脚本运行进程id文件并读取进程id
			fp_pid     = open(pid_file,'r')
			process_id = fp_pid.readlines()
			fp_pid.close()

			###判断pid文件取出的是否是数字
			if not process_id:
				break

			if not re.search(r'^\d',process_id[0]):
				break

			###确认此进程id是否还有进程
			lockcount += 1
			if lockcount > 3:
				write_exec_log('error','1 min after this script is still exists')
				sys.exit(1)
			else:
				if os.popen('ps %s|grep "dzz_mysql_data.py"' % process_id[0]).readlines():
					print "The script is running...... ,Please wait for a moment!"
					time.sleep(20)
				else:
					os.remove(pid_file)
		else:
			break
	###把进程号写入文件
	wp_pid = open(pid_file,'w')
	sc_pid = os.getpid()
	wp_pid.write('%s'% sc_pid)
	wp_pid.close()

###检验端口是否开通函数
def check_ip_telnet(ip,port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect((ip,int(port)))
		s.shutdown(2)
		return True
	except:
		return False

###执行shell命令函数
def exec_shell_cmd(exec_cmd):
        ###执行传入的shell命令
        if exec_cmd:
                (cmd_status,cmd_output) = commands.getstatusoutput(exec_cmd)
        else:
                (cmd_status,cmd_output) = (1,'exec cmd is null')
        ###返回执行状态和输出结果
        return (cmd_status,cmd_output)


###脚本主体
def script_main_body(data_path,do_dir):
	###数据库相应变量
	db_host    = "10.136.0.95"
	create_path = '/data/dzz_create_table.sql'
	if not os.path.isfile(create_path):
		write_exec_log('error','%s not exists' % create_path)
		
	###遍历目录文件
	insert_flag = "ok"
	base_name = do_dir.strip()[:-13]
	data_name = base_name.replace('-','_')
			
	dir_path  = "%s/%s"% (data_path,do_dir.strip()[:-3])
	for do_file in os.listdir(dir_path):
		table_name = "log_%s"% do_file.split("_15_")[0]
		file_path  = "%s/%s"% (dir_path,do_file.strip())		


		creat_cmd = "mysql -uawarmng -p'#SQawar#utL' -h%s -e \"CREATE DATABASE IF NOT EXISTS %s;USE %s;SOURCE %s;\""% (db_host,data_name,data_name,create_path)

		(get_status_creat,get_output_creat) = exec_shell_cmd(creat_cmd)
		if (get_status_creat != 0):
			write_exec_log('error','%s creat data error' % creat_cmd)

		###密令
		load_cmd = "mysql -uawarmng -p'#SQawar#utL' -h%s -e \"USE %s;LOAD DATA local INFILE '%s' IGNORE INTO TABLE %s CHARACTER SET UTF8 FIELDS TERMINATED BY '#@@#' LINES TERMINATED BY '#<>#'\""% (db_host,data_name,file_path,table_name)

		(get_status_load,get_output_load) = exec_shell_cmd(load_cmd)
		if (get_status_load != 0):
			write_exec_log('error','%s load data error' % load_cmd)
			insert_flag = "ng"
			continue
	
	if insert_flag == "ok":
		###把入好的压缩包存放到相应目录
		srv_dir = "/data/all_server/%s"% base_name
		if not os.path.isdir(srv_dir):
			os.makedirs(srv_dir,mode=0777)
				
		###移动文件
		shutil.move("%s/%s"% (data_path,do_dir.strip()),"%s/%s"% (srv_dir,do_dir.strip()))

def all_ip_thread():
	###移动文件
	source_dir = "/data/game_log"
	data_path  = "/data/log_bak"
	for source_file in os.listdir(source_dir):
		shutil.move("%s/%s"% (source_dir,source_file.strip()),"%s/%s"% (data_path,source_file.strip()))

	###读取已经完成的文件
	list_excude = []
	already_fi = "/data/already_insert_mysql.txt" 
	if os.path.isfile(already_fi):
		fp_finish = open(already_fi,'r')
		finish_db = fp_finish.readlines()
		fp_finish.close()

		for excude_tar in finish_db:
			list_excude.append(excude_tar.strip())

	###删除目录
	for tmp_dir in os.listdir(data_path):
		if os.path.isdir("%s/%s"% (data_path,tmp_dir)):
			shutil.rmtree("%s/%s"% (data_path,tmp_dir))

	###解压文件
	list_in = []

	###控制解压文件上限为600
	tar_active = []
	tar_all = [real_tar for real_tar in os.listdir(data_path) if real_tar not in list_excude]
	tar_cou = len(tar_all)
	if tar_cou > 1000:
		tar_active = tar_all[:1000]
	else:
		tar_active = tar_all

	for tar_7z in tar_active:
		if re.search(r'\.7z$',tar_7z):
			extract_num = 1
			while extract_num < 4:
				tar_cmd = "cd %s && /usr/local/bin/7z x %s"% (data_path,tar_7z)
				(get_status_tar,get_output_tar) = exec_shell_cmd(tar_cmd)
				if (get_status_tar != 0):
					write_exec_log('error','%s extract error %d' % (tar_7z,extract_num))
					extract_num += 1
				else:
					list_in.append("%s\n"% tar_7z)
					break
					
	if list_in:	
		fp_have = open(already_fi,'a')
		fp_have.writelines(list_in)
		fp_have.close()

        ###并发调用函数
	threads = []
	for tar_7z in list_in:
		zip_have = re.search(r'\d{1,10}\.7z',tar_7z)
		if zip_have:
			one_bao = threads.append(multiprocessing.Process(target=script_main_body,args=(data_path,tar_7z,)))

	print "current has %d threads" % len(threads)
	###开始多进程
	for start_t in threads:
		start_t.start()

	###阻塞进程
	for join_t in threads:
		join_t.join()
					
if __name__ == "__main__":
	###脚本排它锁
	script_exclusive_lock()

	###主体
	all_ip_thread()

	###程序成功结束
	print "success"
