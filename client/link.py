import socket
import os

os.mkdir("cloud_directory")
# client send
client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
server_addr = ("10.0.15.50", 22)
client_socket.connect(server_addr)
command = "cloud_directory"
client_socket.send(bytes(command, "utf8"))
print('Sent!')

# close
client_socket.close()
