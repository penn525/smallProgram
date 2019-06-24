#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 21, 2019 15:42
# Description: 从服务器下载文件, 使用 UDP 协议

from socket import socket , AF_INET, SOCK_DGRAM
import struct
import time
import os

udp_socket = socket(AF_INET, SOCK_DGRAM)

server_addr = ('192.168.0.***', 69)     # 69为ftpd端口
file_name = b'IMG228.jpg'

# 1, 按 TFTP 协议数据格式, 发送下载请求
down_request = struct.pack('!H10sb5sb', 1, file_name, 0, b'octet', 0)
udp_socket.sendto(down_request, server_addr)

pack_num_list = []
f = ''
while True:
    # 2, 接收数据
    recv_data, recv_addr = udp_socket.recvfrom(1024)
    # print(recv_addr)
    # ('\x00\x03\x00\x01\xff\xd8\xff\xe1', ('192.168.0.***', 51085))

    # 3, 解析出 操作码, 块编码, 包数据
    # 操作码 3 -- 发送正确的下载数据;  5 -- 错误
    oper_code, pack_num = struct.unpack('!HH', recv_data[:4])
    print(oper_code, pack_num)
    # 4, 如果编码为 3 , 将数据写入文件, 并发送 ACK 确认该包已收到
    if oper_code == 3:
        # 当 块编码为1时, 创建新文件
        if pack_num == 1:
            if os.path.exists('gll.jpg'):
                os.remove('gll.jpg')
                print('delete gll.jpg')
            f = open('gll.jpg', 'ab')
        # 块编码是否和上次相同, 不同就写入文件, 并重新发送 ACK
        if pack_num not in pack_num_list:
            f.write(recv_data[4:])
            pack_num_list.append(pack_num)
            print('%d -- 次接收到的数据 ' % pack_num )
        # 发送 ACK 确认包
        ack_data = struct.pack('!HH', 4, pack_num)
        # time.sleep(2)
        udp_socket.sendto(ack_data, recv_addr)
        # 这就是错误的地方， ACK 需要发送到服务器返回的端口
        # udp_socket.sendto(ack_data, server_addr)

        # 数据长度小于 516, 表示最后一个包, 下载完成
        if len(recv_data) < 516:
            print('下载完成')
            f.close()
            break

    # 5, 如果数据为5, 下载错误, 退出循环 
    elif oper_code == 5:
        print('error num: %d ' % pack_num)
        break

udp_socket.close()
