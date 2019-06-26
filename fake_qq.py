#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 24, 2019 10:06
# Description 模拟 QQ 发送和接受消息
'''
需要用到的知识
UDP协议 socket
多线程 使用 concurrent.ThreadPoolExcutor
'''

from socket import AF_INET, SOCK_DGRAM, socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


# 1. 新建socket
class QqClient(object):
    def __init__(self, dest_ip, dest_port, *args, **kwargs):
        # 初始化创建socket
        # 需要更改此处，且不可以写loaclhost 或者 127.0.0.1 ，否则报错
        self.ip_port = ('192.168.0.104', 9000)
        self.dest_ip_port = (dest_ip, int(dest_port))
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind(self.ip_port)

    def send(self):
        # 发送数据
        while True:
            send_data = input('Please Input: ')
            self.client.sendto(send_data.encode(), self.dest_ip_port)
            print('To -> %s[%d]: %s' % (self.dest_ip_port[0],
                                        self.dest_ip_port[1], send_data))

    def receive(self):
        # 接受数据
        while True:
            recv_data, send_addr = self.client.recvfrom(1024)
            print('From <- %s[%d]: %s' %
                  (send_addr[0], send_addr[1], recv_data.decode()))

    def control(self):
        with ThreadPoolExecutor(2) as executor:
            executor.submit(self.send)
            executor.submit(self.receive)

        # thread_send = Thread(target=self.send, name='Thread-Send')
        # thread_recv = Thread(target=self.receive, name='Thread-Recv')
        # try:
        #     thread_send.start()
        #     thread_recv.start()
        #     thread_recv.join()
        #     thread_send.join()
        # except Exception as e:
        #     print(e)
        # finally:
        #     self.client.close()


def main():
    dest_ip = input('please input dest ip: ').strip()
    dest_port = input('please input dest port: ')
    qq = QqClient(dest_ip, dest_port)
    qq.control()


if __name__ == "__main__":
    main()
