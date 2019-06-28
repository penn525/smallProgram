#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 27, 2019 16:00
# Description: select 版本单进程， 多路io复用
'''
思想就是：
    创建监听套接字
    利用某种方法检测被监听的套接字是否可以收发了
    对检测出来的套接字进行收发处理

select和epoll区别
select: 
    连接客户端限制： 32为-1024个连接， 64位-2048个
    检测 的方式时轮询

epoll：
    连接无限制
    检测 的方式为时间触发

'''

from socket import socket, SOL_SOCKET, SO_REUSEADDR
import select

# 1. 创建监听套接字
server_socket = socket()
server_socket.bind(('', 8888))
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.listen()

# 2. 添加需要检测的套接字即相应事件类型
# 注意， epoll只在 linux2.5.4 and newer中可以使用， 在osx中不能用
epoll = select.epoll()
epoll.register(server_socket.fileno(), select.EPOLLIN|select.EPOLLET)

# 分别存储对应的客户端连接信息， fileno为主键
client_sockets = {}
client_addrs = {}

try:
    # 3. 处理套接字
    while True:
        # 检查哪些套接字需要进行收发
        epoll_list = epoll.poll()

        print(epoll_list)

        for fd, events in epoll_list:
            # a. 区分套接字类型以进行相应处理
            # 如果是服务器端，接收连接
            if fd == server_socket.fileno():
                client_socket, client_addr = server_socket.accept()
                # 监听新的套接字
                epoll.register(client_socket.fileno(),
                        select.EPOLLIN|select.EPOLLET)
                
                client_sockets[client_socket.fileno()] = client_socket
                client_addrs[client_socket.fileno()] = client_addr

            # 如果是客户端
            # b. 根据事件类型进行相应的处理
            else:
                if events == select.EPOLLIN:
                    # 有数据要进入，需要读取
                    try:
                        recv_msg = client_sockets[fd].recv(1024).decode()
                    except:
                        # 表示客户端套接字关闭，需要移除监听事件和相应的地址信息
                        print('{} closed!'.format(client_addrs[fd]))
                        epoll.unregister(fd)
                        client_sockets[fd].close()
                        del client_sockets[fd]
                        del client_addrs[fd]
                    else:
                        if recv_msg:
                            print('From {}: {}'.format(client_addrs[fd], recv_msg))
                        else:
                            # 表示客户端套接字关闭，需要移除监听事件和相应的地址信息
                            print('{} closed!'.format(client_addrs[fd]))
                            epoll.unregister(fd)
                            client_sockets[fd].close()
                            del client_sockets[fd]
                            del client_addrs[fd]
                        

finally:
    # 一旦发生异常，需要关闭服务端套接字
    server_socket.close()
    print('Server Closed!')
