# 模拟多个客户端连接

from socket import socket
from random import randint

server_addr = ('', 9999)

socket_list = []
for i in range(10):
    client_socket = socket()
    client_socket.connect(server_addr)
    socket_list.append(client_socket)

while True:
    for s in socket_list:
        s.send(str(randint(0, 100)).encode())
