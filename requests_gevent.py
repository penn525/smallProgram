import gevent
import requests
from requests import socket
urls = ['https://www.baidu.com', 
        'https://www.aliyun.com',
        'http://www.itcast.cn']

jobs = [gevent.spawn(requests.get, url) for url in urls]

results = gevent.joinall(jobs)

cons = [result.value.text for result in results]

for con in cons:
    print(con)



