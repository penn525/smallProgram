#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 25, 2019 23:03
# Description: tcp 客户端

from socket import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

class TcpClient():
    def __init__(self):
        self.dest_ip_port = ('', 8888)
        self.socket_client = socket()
        self.thread_pool = ThreadPoolExecutor(2)

    def start(self):
        self.socket_client.connect(self.dest_ip_port)
        print('Connect to {} Successed!'.format(self.dest_ip_port))
        self.thread_pool.submit(self.handle_recv)
        self.thread_pool.submit(self.handle_send)

    def handle_send(self):
        while True:
            msg = input('To {}: '.format(self.dest_ip_port))
            try:
                self.socket_client.send(msg.encode())
            except Exception as e: 
                print('send closed' + e)
                self.close_socket()
                break
    
    def handle_recv(self):
        while True:
            try:
                data = self.socket_client.recv(1024).decode()
                if data:
                    print(data)
                else:
                    print('Server closed!')
                    self.close_socket()
                    break
            except Exception as e:
                print('recv closed'+ e)
                self.close_socket()
                break

    def close_socket(self):
        if self.socket_client:
            self.socket_client.close()
            self.thread_pool.shutdown()


if __name__ == "__main__":
    tcp_client = TcpClient()
    tcp_client.start()
        
