import socket
import json
import random
import time
import tqdm
import os
from math import ceil

# with open('cloudstore_namenode_conf.json') as json_file:
#     configuration = json.load(json_file)


CURRENT_USER_LOC = ""
USER_TREE = {'':''}


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
        USER_TREE[splitted_path[-2]].append(splitted_path[-1])
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

def files_list_in_dir(dir_name): #ls
    global USER_TREE

    files_list = USER_TREE[dir_name]
    return files_list

def check_dir_files(dir_name):
    global USER_TREE

    temp = len(USER_TREE[dir_name])
    if temp != 0:
        return 1
    else:
        return 0

def command_name(com):
    if command == 0:
        temp = "initialize"
    elif  command == 1:
        temp = "file create"
    elif command == 2: 
        temp = "file read"
    elif command == 3:
        temp = "file write"
    elif command == 4:
        temp = "file delete"
    elif command == 5:
        temp = "file info"
    elif command == 6:
        temp = "file copy"
    elif command == 7:
        temp = "file move"
    elif command == 8:
        temp = "open directory"
    elif command == 9:
        temp = "read directory"
    elif command == 10:
        temp = "make directory"
    elif command == 11:
        temp = "delete directory"
        
    return temp

# init datanodes
datanode1 = ("10.0.0.12", 20001)
datanode2 = ("10.0.0.13", 20001)

datanodes = [datanode1, datanode2]

datanodes_rating = [0 for dn in datanodes]

namenode_datanode_sockets_raw, datanodes_start_info = first_connect(datanodes)

'''
TESTING AREA
'''

# init cloud directory

init_create_cloudstorage(namenode_datanode_sockets_raw, cloud_dir_name="new_cloud_dir")
cd('new_cloud_dir')


down_datanodes = []
namenode_datanode_sockets = []

time.sleep(1)
print('[!] START WORKING')



# server recieve
# server recieve
first_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("10.0.0.11", 2345)
first_server_socket.bind(server_addr)
first_server_socket.listen(1)
first_server_socket.settimeout(2) #

second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr2 = ("10.0.0.11", 2346)
second_server_socket.bind(server_addr2)
second_server_socket.listen(1)
second_server_socket.settimeout(2) #




while True:
    print('wait for connection')
    # (client_socket, addr) = server_socket.accept()

    socket_flag = -1
    while socket_flag == -1:
        try:
            (client_socket, addr) = first_server_socket.accept()
            socket_flag = 0
        except:
            pass
        try:
            (client_socket, addr) = second_server_socket.accept()
            socket_flag = 1
        except:
            pass

    time.sleep(1)
    print('check datanodes')
    for i in range(len(namenode_datanode_sockets_raw)):
        print('check datanode {}'.format(datanodes[i]))
        dsocket = namenode_datanode_sockets_raw[i]
        try:
            # print('send {}'.format(i))
            dsocket.send(bytes("test_message", 'utf8'))
            response = str(dsocket.recv(1024), 'utf8')

            if 'SHUT_UP' in response:
            	down_datanodes.append(i)
            	print('[w] {} is down. Continues without it.'.format(datanodes[i]))
            else:
            	# only workable datanodes
            	namenode_datanode_sockets.append(dsocket)

        except:
            down_datanodes.append(i)
            print('[w] {} is down. Continues without it.'.format(datanodes[i]))


    if len(namenode_datanode_sockets) == 0:
        print("[w] FATAL ERROR. ALL DATANODES DOWN")
        break



    time.sleep(1)
    # create_file(namenode_datanode_sockets, 'tempfile.txt')
    # receive command and arguments
    
    msg = client_socket.recv(1024)
    decoded_msg = str(msg, "utf8")
    if decoded_msg != "":
        print(decoded_msg)
        temp = decoded_msg
        command, argument1, argument2 = temp.split(
            "%"
        )  # argument is file name, directort name and etc.
        command = int(command)
        command_description = command_name(command)
        print("Command id:", command)
        print("TO DO: ", command_description)
        print("Argument01 (file/dir name): ", argument1)
        print("Argument02 (path): ", argument2)
        decoded_msg = ""

        # do smth create, get info etc
        response = ""
        if command == 0:
            # get size of the file
            lost_user(namenode_datanode_sockets)
            init_create_cloudstorage(namenode_datanode_sockets, "new_cloud_dir")
            cd("new_cloud_dir")
            response += "Total size {} \n".format(datanodes_start_info[0][0])
            response += "Used size {} \n".format(datanodes_start_info[0][1])
            response += "Available size {} \n".format(datanodes_start_info[0][2])

            # pass
        elif command == 1:
            # create file
            create_file(namenode_datanode_sockets, argument1)
            response = "File {} is created".format(argument1)
            # pass
        elif command == 2:
            file_name_get = get_file(namenode_datanode_sockets, argument1)
            if file_name_get == False:
                response = "No such file"
                client_socket.send(bytes(response, "utf8"))

            else:
                response = "File {}".format(argument1)
                client_socket.send(bytes(response, "utf8"))
                filename = argument1

                time.sleep(2)
                if socket_flag == 0:
                    ServerIp = "10.0.0.100"
                    PORT = 9899
                else:
                    ServerIp = "10.0.0.101"
                    PORT = 9899
                s = socket.socket()
                
                s.connect((ServerIp, PORT))

                # We can send file sample.txt
                file = open(filename, "rb")
                SendData = file.read(1024)

                while SendData:
                    # Now we can receive data from server
                    # Now send the content of sample.txt to server
                    s.send(SendData)
                    SendData = file.read(1024)

                # Close the connection from client side
                s.close()
                # pass
            # send FILE

        elif command == 3:

            s = socket.socket()

            PORT = 9898
            s.bind(("10.0.0.11", PORT))
            s.listen(10)

            # Now we can establish connection with clien
            conn, addr = s.accept()

            filename = argument1  # should take from client
            # Open one recv.txt file in write mode
            file = open(filename, "wb")
            print("\n Copied file name will be {} at server side\n".format(filename))

            while True:

                # Receive any data from client side
                RecvData = conn.recv(1024)
                while RecvData:
                    file.write(RecvData)
                    RecvData = conn.recv(1024)

                # Close the file opened at server side once copy is completed
                file.close()
                print("\n File has been copied successfully \n")

                # Close connection with client
                conn.close()
                print("\n Server closed the connection \n")

                # Come out from the infinite while loop as the file has been copied from client.
                break
            time.sleep(1)
            upload_file(namenode_datanode_sockets, argument1, argument1)
            # s.close()
            # pass
        elif command == 4:
            # delete file
            delete_file(namenode_datanode_sockets, argument1)
            response = "File {} deleted".format(argument1)
            # pass
        elif command == 5:
            # get info of the file
            f_info = file_info(namenode_datanode_sockets, argument1)

            response += '{} info:\n'.format(argument1)

            for i in range(len(datanodes)):
                response += "-"*len("host : {}\n".format(datanodes[i][0])) + "\n"
                response += "host : {}\n".format(datanodes[i][0])
                response += "\t path : {}\n".format(f_info[i][0])
                response += "\t size : {}\n".format(f_info[i][1])
                response += "-"*len("host : {}\n".format(datanodes[i][0])) + "\n"

        elif command == 6:
            #Create cope of the file
            temp_name_file = argument1 + "-copy"
            create_file(namenode_datanode_sockets, temp_name_file)
            response = "Copy of file {} created as {}".format(argument1, temp_name_file)
            # pass
        elif command == 7:
            #file move (filename, path)
            #get file
            #cd 
            # upload 
            get_file(namenode_datanode_sockets, argument1)
            delete_file(namenode_datanode_sockets, argument1)
            cd(argument2)
            upload_file(namenode_datanode_sockets, argument1, argument1)
            response = "File {} moved to {}".format(argument1, argument2)
            # pass
        elif command == 8:
            #open directore / CD
            res = cd(argument1)
            if res != False:
                response = "Now you are in direcory {}".format(argument1)
            else:
                response = "No such doirectory"
            # pass
        elif command == 9:
            # get list of files
            files_list = files_list_in_dir(argument1)
            response = "\n"
            for i in files_list:
                response = response + i + " \n" 
            response = "Files in the directory {}:".format(argument1) + response
        elif command == 10:
            # create directory
            mkdir(namenode_datanode_sockets, argument1)
            response = "Directory {} is created".format(argument1)
            # pass
        elif command == 11:
            #delete directory
            files_check = check_dir_files(argument1)
            #check if there are files in the dir
            decoded_ans = ""
            if files_check == 1:
                files_list = files_list_in_dir(argument1)
                temp_r = "\n"
                for i in files_list:
                    temp_r = temp_r + i + " \n" 
                response = ("yes/no - Do you want to delete these files too? \n {}".format(temp_r))  # + list of files

                client_socket.send(bytes(response, "utf8"))
                time.sleep(1)
                ans = client_socket.recv(1024)
                decoded_ans = str(ans, "utf8")
                print(decoded_ans)
            else:
                response = "not needed"  # + list of files
                client_socket.send(bytes(response, "utf8"))

                rmdir(namenode_datanode_sockets, argument1)
                decoded_ans == "notNeeded"
                response = "Directory {} deleted\n".format(argument1)
                print(response)



            if decoded_ans == "yes":
                # delete
                rmdir(namenode_datanode_sockets, argument1)
                print("Delete directory: {}".format(argument1))
                response = "Directory {} deleted with files \n {}".format(argument1, files_list)
                # pass
            elif decoded_ans == "no":
                print("Do not delete file: {}".format(argument1))
                response = "Directory {} is not deleted".format(argument1)



        # send response
        if command != 2 and command != 3:
            client_socket.send(bytes(response, "utf8"))



    for i in down_datanodes:
        #try to connect to datanodes if success -> restore from the best
        trial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        before_time = time.clock()
        response = ""
        # print('try {}'.format(i))
        while time.clock() - before_time < 2 and response != 'response':
            try:
                trial_socket.connect(datanodes[i])
                trial_socket.send(bytes('test_message', 'utf8'))
                response = trial_socket.recv(1024)
                response = 'response'
                time.sleep(1)
                init_create_cloudstorage([trial_socket], cloud_dir_name=CURRENT_USER_LOC.split('/')[1])
                namenode_datanode_sockets_raw[i] = trial_socket
                # print('yes')

                time.sleep(1)
                reliable_dn = random.choice([j for j in range(len(datanodes)) if j not in down_datanodes])

                print('[!] Restore {} from {}'.format(datanodes[i], datanodes[reliable_dn]))

                namenode_datanode_sockets_raw[reliable_dn].send(bytes('CODE_RESTORE_4513 {}'.format(datanodes[i][0]), 'utf8'))

                time.sleep(2)

            except:
                # print('no')
                namenode_datanode_sockets_raw[i] = None

    down_datanodes = []
    namenode_datanode_sockets = []
    time.sleep(1)
