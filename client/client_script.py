import socket
import sys
import os
import time

""" it will be read from sys.argv[0]
0 Initialize. 
1 File create.
    file name
2 File read. 
    file name
3 File write. 
    file
4 File delete.
    file name
5 File info. 
    file name
6 File copy. 
    file name
7 File move. 
    file name 
    path
8 Open directory.
    directory name
9 Read directory.
    directory name
10 Make directory.
    directory name
11 Delete directory.
    directory name
"""
""" what receive from namenode
0 text - available size
1 ok
2 FILE  
3 ok
4 ok
5 text - info 
6 ok
7 ok
8 ok 
    should change directory in client too
9 text - list of files
10 ok
11 ok
    need confirmation if there are files in the directory
"""
command = sys.argv[1]
try:
    additional_arg = sys.argv[2]
except:
    additional_arg = ""

try:
    additional_arg_2 = sys.argv[3]  # path
except:
    additional_arg_2 = ""

if command == "initialize":
    command = 0
elif  command == "file_create":
    command = 1
elif command == "file_read": 
    command = 2
elif command == "file_write": 
    command = 3
elif command == "file_delete":
    command = 4
elif command == "file_info": 
    command = 5
elif command == "file_copy":
    command = 6
elif command == "file_move": 
    command = 7
elif command == "open_directory": 
    command = 8
elif command == "read_directory":
    command = 9
elif command == "make_directory":
    command = 10
elif command == "delete_directory":
    command = 11
else:
    print("ERROR: No such command, try again")
    exit(0)
command_id = command

if command_id != 3 and command_id != 2:
    # client send
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ("10.0.0.11", 2345)
    client_socket.connect(server_addr)

    command = str(command) + "%"
    command += additional_arg
    command = str(command) + "%"
    command += additional_arg_2
    client_socket.send(bytes(command, "utf8"))
    print("Sent!")

    """ what to receive 
    0 text - available size
    1 ok
    2 FILE  
    3 ok
    4 ok
    5 text - info 
    6 ok
    7 ok
    8 ok 
        should change directory in client too
    9 text - list of files
    10 ok
    11 ok
        need confirmation if there are files in the directory
    """
    # receive resonse
    if command_id != 2:
        msg = ""
        while msg == "":
            # print(1)
            msg = client_socket.recv(1024)
        # confirmation for deleteing directory with files
        decoded_msg = str(msg, "utf8")
        if decoded_msg != "not needed":
            print(decoded_msg)
            if command_id == 11:
                temp = input()
                client_socket.send(bytes(temp, "utf8"))

    client_socket.close()


elif command_id == 3:
    # client send
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ("10.0.0.11", 2345)
    client_socket.connect(server_addr)
    command = str(command) + "%"
    command += additional_arg
    command = str(command) + "%"
    command += additional_arg_2
    client_socket.send(bytes(command, "utf8"))
    print("Sent!")
    client_socket.close()
    time.sleep(2)
    # send FILE
    ServerIp = "10.0.0.11"
    s = socket.socket()
    PORT = 9898
    s.connect((ServerIp, PORT))
    filename = sys.argv[2]
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
else:

    # client receive
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ("10.0.0.11", 2345)
    client_socket.connect(server_addr)

    command = str(command) + "%"
    command += additional_arg
    command = str(command) + "%"
    command += additional_arg_2
    client_socket.send(bytes(command, "utf8"))
    print("Sent!")
    time.sleep(1)
    msg = ""
    while msg == "":
        # print(1)
        msg = client_socket.recv(1024)
    msg = str(msg, "utf8")
    print(msg)
    client_socket.close()

    if msg != "No such file":
        s = socket.socket()

        PORT = 9899
        s.bind(("10.0.0.100", PORT))
        s.listen(10)

        # Now we can establish connection with clien
        conn, addr = s.accept()

        filename = sys.argv[2]  # should take from client
        # Open one recv.txt file in write mode
        file = open(filename, "wb")

        while True:

            # Receive any data from client side
            RecvData = conn.recv(1024)
            while RecvData:
                file.write(RecvData)
                RecvData = conn.recv(1024)

            # Close the file opened at server side once copy is completed
            file.close()

            # Close connection with client
            conn.close()

            # Come out from the infinite while loop as the file has been copied from client.
            break
        s.close()