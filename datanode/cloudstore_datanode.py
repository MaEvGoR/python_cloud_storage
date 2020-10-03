# datanode service python script
#!/usr/bin/python3

import socket
import os

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




# (namenode_socket, addr) = namenode_datanode_socket.accept()
# msg = namenode_socket.recv(1024)

# decoded_msg = str(msg, "utf8")

# if 'init' == decoded_msg.split()[0]:
# 	new_dir_name = decoded_msg.split()[-1]

# 	current_dir = os.listdir()

# 	# clear directory
# 	# if MAIN_DIR in current_dir:
# 	# 	os.rmdir(MAIN_DIR)

# 	# clear for testing
# 	for item in os.listdir():
# 		if not os.path.isfile(item) and item[0] != '.' :
# 			os.rmdir(item)

# 	# add new directory
# 	os.mkdir(new_dir_name)
# 	MAIN_DIR = new_dir_name
# else:
# 	print("UNKNOWN COMMAND")

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
			os.rmdir(item)

	# add new directory
	os.mkdir(new_dir_name)
	MAIN_DIR = new_dir_name
	print('[!] CREATE MAIN DIRECTORY {}'.format(MAIN_DIR))

def create_file(decoded_msg):
	new_file_name = decoded_msg.split()[-1]
	print('[!] CREATE FILE {}'.format(new_file_name))
	open(WORKING_DIR+new_file_name, 'w').close()

def delete_file(decoded_msg):
	file_name = decoded_msg.split()[-1]
	print('[!] DELETE FILE {}'.format(file_name))
	os.remove(file_name)


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
			'rm' in decoded_msg : delete_file
		}[True]


while True:
	(client_socket, addr) = namenode_datanode_socket.accept()
	while True:
		msg = client_socket.recv(4096)
		decoded_msg = str(msg, 'utf8')
		if decoded_msg != '':
			print('[] FOUND NEW COMMAND <{}>'.format(decoded_msg))
			try:
				function = command_resolver(decoded_msg)
				print(function)
				function(decoded_msg)
			except:
				print('Fuck, i dont know this command or i am stupid: ', decoded_msg)





