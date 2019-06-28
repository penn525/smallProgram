#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 25, 2019 22:26
# Description: tcp 服务端

from socket import socket, SO_REUSEADDR, SOL_SOCKET
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

class TcpServer():
    def __init__(self):
        ip_port = ('', 9090)
        self.server_socket = socket()
        # 解决端口重新绑定问题
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(ip_port)
        self.thread_pool = ThreadPoolExecutor(5)

    def start(self):
        # 主线程用于接收新的连接
        self.server_socket.listen()
        try:
            while True:
                conn = self.server_socket.accept()
                print('Get connection from {}'.format(conn[1]))
                # 没接受到一个连接，交给线程池去处理
                self.thread_pool.submit(self.handle_conn, conn)
                # t = Thread(target=self.handle_conn, args=(conn, ))
                # print(conn)
                # t.start()
                # t.join()
        finally:
            self.server_socket.close()
        
        

    def handle_conn(self, conn):
        # 子线程只负责接收和发送消息
        # 注意， 此部分设计的原理只是给客户端确认， 因此没有添加多线程
        # 如果要求服务端右主动回复的功能， 需要添加线程 
        conn_socket, addr = conn
        while True:
            # 4. 建立连接后， 多线程读写数据
            data = conn_socket.recv(1024).decode()
            if data:
                print('From {} : {}'.format(addr, data))
                conn_socket.send('Hi {}, I got your Msg: {}'.format(addr, data).encode())
                conn_socket.send('Hi {}, I got your Msg: {}'.format(addr, data).encode())
            else:
                print('Connection {} closed!'.format(conn[1]))
                break


if __name__ == "__main__":
    tcp_server = TcpServer()
    tcp_server.start()
