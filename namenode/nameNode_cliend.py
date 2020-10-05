import socket
import tqdm
import os
import time

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
        print("TO DO: ", command)
        print("Argument01: ", argument1)
        print("Argument02: ", argument2)
        decoded_msg = ""

        # do smth create, get info etc
        response = "respone"
        if command == 0:
            # get size of the file
            pass
        elif command == 1:
            # create file
            pass
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
            pass
        elif command == 5:
            # get info of the file
            pass
        elif command == 6:
            pass
        elif command == 7:
            pass
        elif command == 8:
            pass
        elif command == 9:
            # get list of files
            pass
        elif command == 10:
            # create directory
            pass
        elif command == 11:
            response = (
                "yes/no - Do you want to delete these files too?"  # + list of files
            )
            client_socket.send(bytes(response, "utf8"))
            ans = client_socket.recv(1024)
            decoded_ans = str(ans, "utf8")
            print(decoded_ans)
            if decoded_ans == "yes":
                # delete
                print("Delete directory: {}".format(argument1))
                pass
            else:
                print("Do not delete file: {}".format(argument1))

            pass

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

        # send response
        if command != 2 and command != 3:
            client_socket.send(bytes(response, "utf8"))

    # server_socket.close()


server_socket.close()
