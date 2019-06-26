#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 24, 2019 17:08
# Description: udp 广播

import socket

dest_addr = ('<broadcast>', 7788)

broader = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 需要做一下设置才能广播
broader.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print('Broadcast at ', broader.getsockname())

while True:
    broad_msg = input('Server broadcast message: ').encode()
    broader.sendto(broad_msg, dest_addr)
