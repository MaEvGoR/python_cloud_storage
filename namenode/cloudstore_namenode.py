import socket
import json

# with open('cloudstore_namenode_conf.json') as json_file:
# 	configuration = json.load(json_file)


CURRENT_USER_LOC = ""
USER_TREE = {'':''}


namenode_datanode1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

namenode_datanode1_socket.connect(("10.0.0.12", 20001))


# namenode_datanode2_socket = socket.socket(socket.AF_INET,
#                               socket.SOCK_STREAM)

# namenode_datanode2_socket.connect(("10.0.0.13", 20001))

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


def init_create_cloudstorage(my_socket, cloud_dir_name="cloud_dir"):
    my_socket.send(bytes("init {}".format(cloud_dir_name), "utf8"))
    USER_TREE[''] = [cloud_dir_name]
    USER_TREE[cloud_dir_name] = []


def create_file(my_socket, filename="temp_file.txt"):

	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split("/")
	if find_path(USER_TREE, splitted_path[1], splitted_path[-1]):
		print(USER_TREE)
		print(splitted_path)
		return False
	else:
		USER_TREE[splitted_path[-2]].append(filename)

	my_socket.send(bytes("touch {}".format(req_location), "utf8"))
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


def delete_file(my_socket, filename="temp_file.txt"):
	req_location = "{}/{}".format(CURRENT_USER_LOC, filename)
	splitted_path = req_location.split("/")
	if USER_TREE[splitted_path[-1]] == filename:
		USER_TREE[splitted_path[-1]].remove(filename)
	else:
		print('I fucked up in deleting file')
		return False

	my_socket.send(bytes("rm {}".format(req_location), "utf8"))
	print('[!] SEND COMMAND ', "rm {}".format(req_location))


# init cloud directory

init_create_cloudstorage(namenode_datanode1_socket, cloud_dir_name="new_cloud_dir")
cd('new_cloud_dir')
create_file(namenode_datanode1_socket, filename="tempfile.txt")

# init_create_cloudstorage(namenode_datanode2_socket, cloud_dir_name='new_cloud_dir')


















