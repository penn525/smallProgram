#! /usr/bin python
# -*- coding: utf-8 -*-
# Author: wupeng
# Time: Jun 27, 2019 19:51
# Description: 
'''
协程可以认为是比线程更小的执行单元，因为他自带CPU上下文。
这样在合适的时机，可以由一个协程切换到另一个协程。

在python中是通过generator实现的

利用协程解决生产者-消费者问题

协程相比较于线程的优点：
    1. 线程切换比较消耗资源，写成效率比较高
    2. 协程不需要锁,由于只有一个线程，不存在同时写冲突

最高的效率应该是：
    多进程 + 协程
'''

def consumer():
    print('Start consumer')
    r = ''
    while True:
        " 3. 接收生产者信息，直接让生产者去生产 "
        " 7. 消费完成后， 告诉生产者 "
        n = yield r
        " 5. 拿到n后， 判断有， 去消费 "
        if not n:
            return
        "6. 消费者接受到生产了一个， 并进行消费"
        print('[CONSUMER] Consuming %s ...' % n)
        r = '200 OK'


def produce(c):
    "1. 开始进行生产"
    print('Start Produce')
    "2. 告诉comsumer，目前没有产品"
    "首先调用c.send(None)启动生成器；"
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        " 4. 生产者生产了一个产品， 并且告诉消费者，让他去消费 "
        r = c.send(n)
        " 8. 生产者接受到消费者消费完成的信息，并进行下一个生产 "
        print('[PRODUCER] Consumer return: %s ' % r)
    c.close()

c = consumer()
produce(c)
