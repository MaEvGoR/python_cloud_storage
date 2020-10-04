import socket
import json
import random
import time

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
	
	for addr in addrs:
		cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cur_socket.connect(addr)
		namenode_datanode_sockets.append(cur_socket)

	return namenode_datanode_sockets


# namenode_datanode1_socket.send(bytes("TEST Message from namenode to datanode1", "utf8"))
# namenode_datanode2_socket.send(bytes("TEST Message from namenode to datanode2", "utf8"))



'''
TODO same name of directory in different directories
'''

def choose_sockets(namenode_datanode_sockets):
	return random.sample(namenode_datanode_sockets, REPLICA_PARAM)


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
	if find_path(USER_TREE, splitted_path[-1], target.split('/')[-1]):
		CURRENT_USER_LOC += '/{}'.format(target)
	else:
		print(USER_TREE)
		print(CURRENT_USER_LOC)
		print(target)


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
		dsocket.send(bytes("rm {}".format(req_location), "utf8"))
	print('[!] SEND COMMAND ', "rm {}".format(req_location))

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

# init datanodes
datanode1 = ("10.0.0.12", 20001)
datanode2 = ("10.0.0.13", 20001)

namenode_datanode_sockets = first_connect([datanode1, datanode2])


'''
TESTING AREA
'''

# init cloud directory

init_create_cloudstorage(namenode_datanode_sockets, cloud_dir_name="new_cloud_dir")

# get into this cloud directory
cd('new_cloud_dir')
time.sleep(1)

# create file in this directory
create_file(namenode_datanode_sockets, filename="tempfile.txt")

time.sleep(1)

# delete this file
# delete_file(namenode_datanode_sockets[0], filename="tempfile.txt")

time.sleep(1)

mkdir(namenode_datanode_sockets, dir_name="my_new_dir")

time.sleep(1)

mkdir(namenode_datanode_sockets, dir_name="my_new_dir2")

time.sleep(1)

rmdir(namenode_datanode_sockets, dir_name="my_new_dir")










