#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 26, 2019 17:49
# Description: 利用非阻塞模拟多线程或者多进程
'''
思想就是类似 CPU 
只要不阻塞，且数据处理的较快，可以模拟多线程
'''

from socket import socket, SOL_SOCKET, SO_REUSEADDR

server_socket = socket()
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# 设置 socket 非阻塞
# 此时accept时，弱国收不到x=connect 请求， 将报错
server_socket.setblocking(False)
server_socket.bind(('', 9999))
server_socket.listen(10)

client_list = []
while True:
    try:
        # 无限循环接收连接， 查看是否有消息
        client_info = server_socket.accept()
    except:
        pass
    else:
        client_list.append(client_info)
        print('Client {} connected! '.format(client_info[1]))
        client_list.append(client_info)

    # 每次循环，需要删除的客户端信息
    # 之所以放在这里，是由于尽量不要变便利边删除， 且一起删除有效率
    client_to_del = []

    for client in client_list:
        client_socket, client_addr = client
        try:
            data = client_socket.recv(1024).decode()
        except: 
            pass
        else:
            if data:
                print('{}: {} '.format(client_addr, data))
            else:
                print('Client {} closed! '.format(client_addr))
                client_to_del.append(client)

    # 同一删除需要删除的socket 
    for client in client_to_del:
        client_list.remove(client)
