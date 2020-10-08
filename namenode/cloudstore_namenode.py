import socket
import json
import random
import time
import tqdm
import os
from math import ceil

# with open('cloudstore_namenode_conf.json') as json_file:
# 	configuration = json.load(json_file)


CURRENT_USER_LOC = ""
USER_TREE = {'':''}
REPLICA_PARAM = 2


# namenode_datanode1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# namenode_datanode1_socket.connect(("10.0.0.12", 20001))


# namenode_datanode2_socket = socket.socket(socket.AF_INET,
#                               socket.SOCK_STREAM)

# namenode_datanode2_socket.connect(("10.0.0.13", 20001))

def first_connect(addrs):
	namenode_datanode_sockets = []
	start_info = []
	for addr in addrs:
		cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cur_socket.connect(addr)

		total, used, free = map(int, str(cur_socket.recv(1024), 'utf8').split('<SEPARATOR>'))

		namenode_datanode_sockets.append(cur_socket)
		start_info.append([(total // (2**30)), (used // (2**30)), (free // (2**30))])

	return namenode_datanode_sockets, start_info



# namenode_datanode1_socket.send(bytes("TEST Message from namenode to datanode1", "utf8"))
# namenode_datanode2_socket.send(bytes("TEST Message from namenode to datanode2", "utf8"))



'''
TODO same name of directory in different directories
'''


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph.keys():
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None


def init_create_cloudstorage(my_sockets, cloud_dir_name="cloud_dir"):

	global USER_TREE

	for dsocket in my_sockets:
		dsocket.send(bytes("init {}".format(cloud_dir_name), "utf8"))

	USER_TREE[''] = [cloud_dir_name]
	USER_TREE[cloud_dir_name] = []


def create_file(my_sockets, filename="temp_file.txt"):

	global USER_TREE
	global CURRENT_USER_LOC

	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split("/")
	if find_path(USER_TREE, splitted_path[1], splitted_path[-1]):
		print(USER_TREE)
		print(splitted_path)
		return False
	else:
		USER_TREE[splitted_path[-2]].append(filename)

	for dsocket in my_sockets:
		dsocket.send(bytes("touch {}".format(req_location), "utf8"))
	print('[!] SEND COMMAND ', "touch {}".format(req_location))

def cd(target):

	global CURRENT_USER_LOC

	splitted_path = CURRENT_USER_LOC.split('/')
	# / in the end of directory path
	if target == '..':
		CURRENT_USER_LOC = ''
		for i in range(1, len(splitted_path)-1):
			CURRENT_USER_LOC += '/{}'.format(splitted_path[i])

		return True

	if target == '':
		CURRENT_USER_LOC = '/' + splitted_path[1]

		return True

	if find_path(USER_TREE, splitted_path[-1], target.split('/')[-1]):
		CURRENT_USER_LOC += '/{}'.format(target)
	else:
		print(USER_TREE)
		print(CURRENT_USER_LOC)
		print(target)

		return False


def delete_file(my_sockets, filename="temp_file.txt"):

	global USER_TREE
	global CURRENT_USER_LOC

	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split("/")
	if filename in USER_TREE[splitted_path[-2]]:
		USER_TREE[splitted_path[-2]].remove(splitted_path[-1])
	else:
		print('[w] Something goes wrong with deleting file {}'.format(filename))
		return False

	for dsocket in my_sockets:
		dsocket.send(bytes("rmfile {}".format(req_location), "utf8"))
	print('[!] SEND COMMAND ', "rmfile {}".format(req_location))

def mkdir(my_sockets, dir_name="name_dir"):

	global USER_TREE

	req_location = "{}/{}".format(CURRENT_USER_LOC, dir_name)
	splitted_path = req_location.split('/')
	if find_path(USER_TREE, splitted_path[1], splitted_path[-2]):
		USER_TREE[splitted_path[-2]].append(splitted_path[-1])
		USER_TREE[dir_name] = []
	else:
		print('[w] Something goes wrong with creating directory {}'.format(filename))
		return False
	for dsocket in my_sockets:
		dsocket.send(bytes("mkdir {}".format(req_location), "utf8"))
	print('[!] SEND COMMAND ', "mkdir {}".format(req_location))

def rmdir(my_sockets, dir_name="name_dir"):

	global USER_TREE

	req_location = "{}/{}".format(CURRENT_USER_LOC, dir_name)
	splitted_path = req_location.split('/')
	if find_path(USER_TREE, splitted_path[1], splitted_path[-1]):
		USER_TREE[splitted_path[-2]].remove(splitted_path[-1])
		USER_TREE.pop(splitted_path[-1], None)
	else:
		print('[w] Something goes wrong with deleting directory {}'.format(splitted_path[-1]))
		return False
	for dsocket in my_sockets:
		dsocket.send(bytes("rmdir {}".format(req_location), 'utf8'))
	print('[!] SEND COMMAND ', "rmdir {}".format(req_location))

def lost_user(my_sockets):

	global USER_TREE
	global CURRENT_USER_LOC

	print('[w] I lost my user. Sending signal to datanodes.')
	for dsocket in my_sockets:
		dsocket.send(bytes('CODE_END_3085', 'utf8'))
	USER_TREE = {'':''}
	CURRENT_USER_LOC = ''

def get_file(my_sockets, filename="temp_file.txt"):

	global USER_TREE
	global CURRENT_USER_LOC

	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split('/')
	if find_path(USER_TREE, splitted_path[1], splitted_path[-2]) and splitted_path[-1] in USER_TREE[splitted_path[-2]]:
		pass
	else:
		print('[w] Something goes wrong with downloading file {}'.format(splitted_path[-1]))
		return False

	dsocket = random.choice(my_sockets)
	dsocket.send(bytes('get_file {}'.format(req_location), 'utf8'))

	print('[!] SEND COMMAND get_file {}'.format(req_location))
	print('[!] WAITING FOR THE FILE {}'.format(req_location))

	time.sleep(1)


	# get info about file
	info_msg = str(dsocket.recv(1024), 'utf8')
	filename, filesize = info_msg.split('<SEPARATOR>')

	print('[!] GET INFO: {} {}'.format(filename, filesize))

	filesize = int(filesize)
	filename = os.path.basename(filename)

	progress = tqdm.tqdm(range(int(ceil(filesize/8))), "Receiving {}".format(filename), unit="B", unit_scale=True, unit_divisor=8)
	with open(filename, "wb") as f:
		for _ in progress:

			bytes_read = dsocket.recv(8)
			if not bytes_read:
				break
			f.write(bytes_read)
			progress.update(len(bytes_read))

	print('[!] RECIEVED FILE {}'.format(filename))

	return filename


def upload_file(my_sockets, local_fname="tempfile.txt", server_filename="tempfile.txt"):

	global USER_TREE
	global CURRENT_USER_LOC

	req_location = "{}/{}".format(CURRENT_USER_LOC, server_filename)
	splitted_path = req_location.split('/')

	if find_path(USER_TREE, splitted_path[1], splitted_path[-2]):
		pass
	else:
		print('[w] Something goes wrong with uploading file {}'.format(splitted_path[-1]))
		return False

	if splitted_path[-1] in USER_TREE[splitted_path[-2]]:
		delete_file(my_sockets, server_path)

	for dsocket in my_sockets:
		dsocket.send(bytes('upload {}'.format(req_location), 'utf8'))

	print('[!] Send upload {}'.format(req_location))

	time.sleep(1)

	file_path = local_fname
	file_size = os.path.getsize(file_path)

	try:

		for dsocket in my_sockets:
			dsocket.send(bytes("{}<SEPARATOR>{}".format(file_path, file_size), 'utf8'))

		time.sleep(1)

		progress = tqdm.tqdm(range(int(ceil(file_size/8))), "Sending {}".format(file_path), unit="B", unit_scale=True, unit_divisor=8)
		with open(local_fname, 'rb') as f:
				for _ in progress:
					bytes_read = f.read(8)
					
					if not bytes_read:
						break

					for dsocket in my_sockets:
						dsocket.sendall(bytes_read)

					progress.update(len(bytes_read))
		print('[!] Upload  file {}'.format(file_path))
	except:
		print('[w] Something goes wrong with uploading file {}')


def file_info(my_sockets, filename="tempfile.txt"):

	global USER_TREE
	global CURRENT_USER_LOC

	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split('/')
	if find_path(USER_TREE, splitted_path[1], splitted_path[-2]) and splitted_path[-1] in USER_TREE[splitted_path[-2]]:
		pass
	else:
		print('[w] Something goes wrong with information about file {}'.format(splitted_path[-1]))
		return False

	info = []

	print('[!] Send info {}'.format(req_location))

	for dsocket in my_sockets:
		dsocket.send(bytes('info {}'.format(req_location), 'utf8'))

		response = str(dsocket.recv(1024), 'utf8').split()

		info.append(response)

	return info



# init datanodes
datanode1 = ("10.0.0.12", 20001)
datanode2 = ("10.0.0.13", 20001)

datanodes = [datanode1, datanode2]

namenode_datanode_sockets, datanodes_start_info = first_connect(datanodes)

print(datanodes_start_info)


'''
TESTING AREA
'''

# init cloud directory

init_create_cloudstorage(namenode_datanode_sockets, cloud_dir_name="new_cloud_dir")

# get into this cloud directory

cd('new_cloud_dir')

time.sleep(1)

# # create file in this directory
# create_file(namenode_datanode_sockets, filename="tempfile.txt")

mkdir(namenode_datanode_sockets, dir_name="new_dir1")

time.sleep(1)

cd("new_dir1")

time.sleep(1)

create_file(namenode_datanode_sockets, filename='smth.txt')

time.sleep(1)

cd('..')

time.sleep(1)

create_file(namenode_datanode_sockets, filename='smth2.txt')

time.sleep(1)

mkdir(namenode_datanode_sockets, dir_name="new_dir2")

time.sleep(1)

cd("new_dir2")

time.sleep(1)

mkdir(namenode_datanode_sockets, dir_name="new_dir3")

time.sleep(1)

create_file(namenode_datanode_sockets, filename='smth3.txt')

time.sleep(1)

cd("new_dir3")

time.sleep(1)

upload_file(namenode_datanode_sockets, local_fname="tempfile.txt", server_filename="tempfile.txt")

time.sleep(1)

cd('..')

time.sleep(1)

cd('..')

time.sleep(1)

rmdir(namenode_datanode_sockets, dir_name="new_dir1")

time.sleep(1)

print(file_info(namenode_datanode_sockets, filename='smth2.txt'))

# delete this file
# delete_file(namenode_datanode_sockets[0], filename="tempfile.txt")

# time.sleep(1)

# mkdir(namenode_datanode_sockets, dir_name="my_new_dir")

# time.sleep(1)

# mkdir(namenode_datanode_sockets, dir_name="my_new_dir2")

# time.sleep(1)

# rmdir(namenode_datanode_sockets, dir_name="my_new_dir")

# time.sleep(1)



























