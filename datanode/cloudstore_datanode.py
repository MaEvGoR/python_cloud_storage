# datanode service python script
#!/usr/bin/python3

import socket
import os
import shutil
import tqdm
import time
from math import ceil

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

def send_file(decoded_msg, nsocket):
	file_path = decoded_msg.split()[-1]
	
	# # start just for test
	# with open(file_path[1:], 'w') as f:
	# 	f.write('5'*100)
	# # end just for test


	file_size = os.path.getsize(file_path[1:])


	try:
		nsocket.send(bytes('{}<SEPARATOR>{}'.format(file_path, file_size), 'utf8'))

		time.sleep(1)

		progress = tqdm.tqdm(range(int(ceil(file_size/8))), "Sending {}".format(file_path), unit="B", unit_scale=True, unit_divisor=8)
		with open(file_path[1:], 'rb') as f:
			for _ in progress:
				bytes_read = f.read(8)
				
				if not bytes_read:
					break

				nsocket.sendall(bytes_read)
				progress.update(len(bytes_read))

		print('[!] SEND FILE {}'.format(file_path))

	except:
		print('[w] CANNOT SEND FILE {}'.format(file_path))

def download_file(decoded_msg, nsocket):
	file_path = decoded_msg.split()[-1]

	info_msg = str(nsocket.recv(1024), 'utf8')
	filename, filesize = info_msg.split('<SEPARATOR>')

	filesize = int(filesize)

	print('[!] GET INFO: {} {}'.format(filename, filesize))

	progress = tqdm.tqdm(range(int(ceil(filesize/8))), "Receiving {}".format(filename), unit="B", unit_scale=True, unit_divisor=8)
	with open(file_path[1:], "wb") as f:
		for _ in progress:

			bytes_read = nsocket.recv(8)

			
			if not bytes_read:
				break

			f.write(bytes_read)
			progress.update(len(bytes_read))

	print('[!] RECEIVED FILE {}'.format(filename))

	return filename

def logout(decoded_msg):

	global MAIN_DIR
	MAIN_DIR = ''

def restore_other_datanode(decoded_msg):

	global MAIN_DIR

	target_host = decoded_msg.split()[-1]

	os.system('scp -r {} vagrant@{}:'.format(MAIN_DIR, target_host))



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
			'rmfile' in decoded_msg : delete_file,
			'CODE_END_3085' in decoded_msg : logout,
			'CODE_RESTORE_4513' in decoded_msg : restore_other_datanode,
			'mkdir' in decoded_msg : create_dir,
			'rmdir' in decoded_msg : rmdir,
			'get_file' in decoded_msg or 'upload' in decoded_msg or 'info' in decoded_msg: None,
		}[True]

def datanode_info_start(client_socket):

	total, used, free = shutil.disk_usage("/")
	client_socket.sendall(bytes("{}<SEPARATOR>{}<SEPARATOR>{}".format(total, used, free), 'utf8'))
	time.sleep(1)

def file_info(decoded_msg, nsocket):
	file_path = decoded_msg.split()[-1]
	try:
		file_size = os.path.getsize(file_path[1:])
	except:
		print('[w] CANNOT FIND FILE ', file_path)

	nsocket.send(bytes('{} {}'.format(file_path, file_size), 'utf8'))

	time.sleep(1)




while True:
	try:
		(client_socket, addr) = namenode_datanode_socket.accept()
	except KeyboardInterrupt:
		client_socket.send(bytes('SHUT_UP', 'utf8'))
		namenode_datanode_socket.shutdown(socket.SHUT_RDWR)
		namenode_datanode_socket.close()
		exit(0)

	datanode_info_start(client_socket)
	print('[!] GET NEW CONNECTION {}'.format(addr))
	decoded_msg = ''
	try:
		while True:
			try:
				msg = client_socket.recv(1024)
			except:
				break

			decoded_msg = str(msg, 'utf8')

			if decoded_msg != '':
				if 'test_message' in decoded_msg:
					client_socket.send(bytes('response', 'utf8'))
					decoded_msg = decoded_msg.split('test_message')[1]

				if decoded_msg == '':
					continue

				print('[] FOUND NEW COMMAND <{}>'.format(decoded_msg))
				try:
					function = command_resolver(decoded_msg)
					if function == None:
						if 'get_file' in decoded_msg:
							print(send_file)
							send_file(decoded_msg, client_socket)	
						elif 'upload' in decoded_msg:
							print(download_file)
							download_file(decoded_msg, client_socket)
						elif 'info' in decoded_msg:
							print(file_info)
							file_info(decoded_msg, client_socket)
					else:
						print(function)
						function(decoded_msg)
				except:
					print('Fuck, i dont know this command or i am stupid or i got end signal: ', decoded_msg)
				print('-----------------')
	except KeyboardInterrupt:
		namenode_datanode_socket.close()
		exit(0)

	print('-----------------')
	print('[w] LOST CONNECTION WITH NAMENODE')
	print('-----------------')
