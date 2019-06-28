'''
greenlet 方便协程切换
'''

from greenlet import greenlet
import time


def consumer(n):
    r = ''
    while True:
        n = gr_p.switch(r)
        if not n:
            return
        print('[Consumer] consuming %s ...' % n)
        r = '200 OK'

def producer(r):
    r = gr_c.switch(None)
    n = 0
    while n < 5:
        n += 1
        print('[Producer] porduced %s ...' % n)
        r = gr_c.switch(n)
        print('[Producer] Consumer return %s ...' % r)


gr_c = greenlet(consumer)
gr_p = greenlet(producer)

gr_p.switch(None)
