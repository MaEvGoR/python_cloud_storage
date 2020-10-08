import socket
import os
import time

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


""" it will be revieved from client
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
    file name & path
8 Open directory.
    directory name
9 Read directory.
    directory name
10 Make directory.
    directory name
11 Delete directory.
    directory name
"""

# server recieve
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("10.0.0.11", 2345)
server_socket.bind(server_addr)
server_socket.listen(1)

while True:
    # receive command and arguments
    (client_socket, addr) = server_socket.accept()
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
        response = "respone"
        if command == 0:
            # get size of the file
            pass
        elif command == 1:
            # create file
            # create_file(namenode_datanode_sockets, argument1)
            response = "File {} is created".format(argument1)
            # pass
        elif command == 2:
            time.sleep(2)
            print("tuta")
            # send FILE
            ServerIp = "10.0.0.100"
            s = socket.socket()
            PORT = 9899
            s.connect((ServerIp, PORT))

            filename = argument1
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
        elif command == 3:

            s = socket.socket()

            PORT = 9898
            s.bind(("10.0.0.11", PORT))
            s.listen(10)

            # Now we can establish connection with clien
            conn, addr = s.accept()

            filename = "new_" + argument1  # should take from client
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
            # s.close()
            # pass
        elif command == 4:
            # delete file
            # delete_file(namenode_datanode_sockets, argument1)
            response = "File {} deleted".format(argument1)
            # pass
        elif command == 5:
            # get info of the file

            pass
        elif command == 6:
            #Create cope of the file
            temp_name_file = argument1 + "-copy"
            # create_file(namenode_datanode_sockets, temp_name_file)
            response = "Copy of file {} created as {}".format(argument1, temp_name_file)
            # pass
        elif command == 7:
            #file move (filename, path)
            pass
        elif command == 8:
            #open directore / CD
            # cd(argument1)
            response = "Now you are in direcory {}".format(argument1)
            # pass
        elif command == 9:
            # get list of files
            # files_list = files_list_in_dir(argument1)
            # for i in files_list:
            #     temp = str(i)
            #     response = response + temp + " \n" 
            response = "Files in the directory {}:".format(argument1) + response
        elif command == 10:
            # create directory
            # mkdir(namenode_datanode_sockets, argument1)
            response = "Directory {} is created".format(argument1)
            # pass
        elif command == 11:
            #delete directory
            files_check = check_dir_files(argument1)
            #check if there are files in the dir
            if files_check = 1:
                files_list = files_list_in_dir(argument1)
                for i in files_list:
                    temp = str(i)
                    response = response + temp + " \n" 
                response = ("yes/no - Do you want to delete these files too? \n {}".format(files_list))  # + list of files
                client_socket.send(bytes(response, "utf8"))
                ans = client_socket.recv(1024)
                decoded_ans = str(ans, "utf8")
                print(decoded_ans)

            if decoded_ans == "yes":
                # delete
                rmdir(namenode_datanode_sockets, argument1)
                print("Delete directory: {}".format(argument1))
                response = "Directory {} deleted with files \n {}".format{argument1, files_list}
                # pass
            else:
                print("Do not delete file: {}".format(argument1))
                response = "Directory {} is not deleted".format{argument1}



        # send response
        if command != 2 and command != 3:
            client_socket.send(bytes(response, "utf8"))

    # server_socket.close()


server_socket.close()
