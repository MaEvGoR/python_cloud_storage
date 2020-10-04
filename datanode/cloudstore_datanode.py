# datanode service python script
#!/usr/bin/python3

import socket
import os
import shutil

WORKING_DIR = '/home/vagrant'
MAIN_DIR = ''


os.chdir(WORKING_DIR)

# Initialization

namenode_datanode_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if socket.gethostname() == 'datanode1':
	datanode_addr = ("10.0.0.12", 20001)

if socket.gethostname() == 'datanode2':
	datanode_addr = ("10.0.0.13", 20001)

namenode_datanode_socket.bind(datanode_addr)
namenode_datanode_socket.listen(1000)


def create_main_dir(decoded_msg):

	global MAIN_DIR

	print('[] FOUND NEW USER')
	new_dir_name = decoded_msg.split()[-1]
	current_dir = os.listdir()

	# clear directory
	# if MAIN_DIR in current_dir:
	# 	os.rmdir(MAIN_DIR)

	# clear for testing
	for item in os.listdir():
		if not os.path.isfile(item) and item[0] != '.' :
			try:
				shutil.rmtree(item)
			except:
				print('[w] Tried delete {}, but something goes wrong'.format(item))

	# add new directory
	os.mkdir(new_dir_name)
	MAIN_DIR = new_dir_name
	print('[!] CREATE MAIN DIRECTORY {}'.format(MAIN_DIR))

def create_file(decoded_msg):
	new_file_name = decoded_msg.split()[-1]
	open(WORKING_DIR+new_file_name, 'w').close()
	print('[!] CREATE FILE {}'.format(new_file_name))

def delete_file(decoded_msg):
	file_name = decoded_msg.split()[-1]
	os.remove(WORKING_DIR+file_name)
	print('[!] DELETE FILE {}'.format(file_name))

def create_dir(decoded_msg):
	dir_path = decoded_msg.split()[-1]
	try:
		os.mkdir(dir_path[1:])
		print('[!] CREATE DIRECTORY {}'.format(dir_path))
	except:
		print('[w] CANNOT CREATE DIRECTORY {}'.format(dir_path))

def rmdir(decoded_msg):
	dir_path = decoded_msg.split()[-1]
	try:
		shutil.rmtree(dir_path[1:])
		print('[!] DELETE DIRECTORY {}'.format(dir_path))
	except:
		print('[w] CANNOT DELETE DIRECTORY {}'.format(dir_path))


def logout(decoded_msg):

	global MAIN_DIR
	MAIN_DIR = ''


def command_resolver(decoded_msg):

	if MAIN_DIR == '':
		if 'init' == decoded_msg.split()[0]:
			# create_main_dir(decoded_msg)
			return create_main_dir
		else:
			return None
	else:
		return {
			'touch' in decoded_msg : create_file,
			'rm' in decoded_msg : delete_file,
			'CODE_END_3085' in decoded_msg : logout,
			'mkdir' in decoded_msg : create_dir,
			'rmdir' in decoded_msg : rmdir,
		}[True]


while True:
	(client_socket, addr) = namenode_datanode_socket.accept()
	print('[!] GET NEW CONNECTION {}'.format(addr))
	decoded_msg = ''
	while True:
		msg = client_socket.recv(1024)

		decoded_msg = str(msg, 'utf8')

		if decoded_msg != '':
			print('[] FOUND NEW COMMAND <{}>'.format(decoded_msg))
			try:
				function = command_resolver(decoded_msg)
				print(function)
				function(decoded_msg)
			except:
				print('Fuck, i dont know this command or i am stupid or i got end signal: ', decoded_msg)
			print('-----------------')
	print('-----------------')
	print('[w] LOST CONNECTION WITH NAMENODE')
	print('-----------------')





