import socket
import sys

""" it will be read from sys.argv[0]
0 Initialize. 
1 File create.
2 File read. 
3 File write. 
4 File delete.
5 File info. 
6 File copy. 
7 File move. 
8 Open directory.
9 Read directory.
10 Make directory.
11 Delete directory.
"""

# client send
client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
server_addr = ("10.0.15.50", 22)
client_socket.connect(server_addr)
command = sys.argv[1]
client_socket.send(bytes(command, "utf8"))
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
    print(msg)
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
    '''
        do smth with the received file
    '''
    pass