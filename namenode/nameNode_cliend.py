import socket
""" it will be revieved from client
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

# server receive


server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
server_addr = ("10.0.15.50", 22)
server_socket.bind(server_addr)
server_socket.listen(1000)
(client_socket, addr) = server_socket.accept()

msg = client_socket.recv(1024)
print(msg)
# close
server_socket.close()

if msg != 11:
    '''

    do smth with the command from msg

    '''

if msg == 11:
    # confirmation if msg = 11
    '''

    if there are files in this directory
    then get this list of the files

    '''
    response = "yes/no - Do you want to delete these files too?"  # + list of files
    # send confirmation
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    client_socket.connect(server_addr)
    client_socket.send(bytes(response, "utf8"))
    print('Sent!')
    client_socket.close()
    # receive confirmation
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    server_addr = ("10.0.15.50", 22)
    server_socket.bind(server_addr)
    server_socket.listen(1000)
    (client_socket, addr) = server_socket.accept()

    msg = client_socket.recv(1024)
    if msg == "yes":
        '''
        
        delete this directory
        
        '''
    # close
    server_socket.close()


''' what to send as a response 
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

if msg == 1:
    '''
    
    # get size of the file
    
    '''
    response = 0
elif msg == 2:
    '''
    
    # get the file
    
    '''
    response = 2
elif msg == 5:
    '''
    
    #get info of the file
    
    '''
    response = "info"
elif msg == 9:
    '''
    
    get list of files
    
    '''
    response = "list of files"
else:
    response = "ok"

# server send response
client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
client_socket.connect(server_addr)
client_socket.send(bytes(response, "utf8"))
print('Sent!')
client_socket.close()