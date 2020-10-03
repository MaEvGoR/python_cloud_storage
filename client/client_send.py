import socket
import sys
import os
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

if sys.argv[1] != 3:
	# client send
	client_socket = socket.socket(socket.AF_INET,
	                              socket.SOCK_STREAM)
	server_addr = ("10.0.15.50", 22)
	client_socket.connect(server_addr)
	command = sys.argv[1]
	try:
		additional_arg = sys.argv[2]
	except:
		additional_arg = '' 
	temp = command
	command = str(temp) + '_'
	command += additional_arg	
	client_socket.send(bytes(command, "utf8"))
	print('Sent!')

	# close
	client_socket.close()
else:
	# client send 3
	client_socket = socket.socket(socket.AF_INET,
	                              socket.SOCK_STREAM)
	server_addr = ("10.0.15.50", 22)
	client_socket.connect(server_addr)
	command = sys.argv[1]	
	temp = command
	command = str(temp) + '_'
	client_socket.send(bytes(command, "utf8"))
	print('Sent!')
	client_socket.close()


	# client send file
	client_socket = socket.socket(socket.AF_INET,
	                              socket.SOCK_STREAM)
	server_addr = ("10.0.15.50", 22)
	client_socket.connect(server_addr)
	filename = sys.argv[2]
	filesize = os.path.getsize(filename)
	client_socket.send("{}{}{}".format(filename, sep, filesize).encode())

	print('Sent!')

	# close
	client_socket.close()

''' what to receive 
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
'''

# client receive response
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
server_addr = ("10.0.15.50", 22)
server_socket.bind(server_addr)
server_socket.listen(1000)
(client_socket, addr) = server_socket.accept()
server_socket.close()


msg = client_socket.recv(1024)
if msg != 2:
    print ("File downloaded succesfully" )
elif msg == 11:
    # recieve confirmation
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    server_addr = ("10.0.15.50", 22)
    server_socket.bind(server_addr)
    server_socket.listen(1000)
    (client_socket, addr) = server_socket.accept()
    print (msg)
    a = input
    server_socket.close()
    #send confirmation
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    server_addr = ("10.0.15.50", 22)
    client_socket.connect(server_addr)
    command = sys.argv[1]
    client_socket.send(bytes(command, "utf8"))
    client_socket.close()
else:
    print(msg)