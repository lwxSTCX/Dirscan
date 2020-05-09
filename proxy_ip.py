#coding=utf-8
#获取最新ip地址

import requests
import threading
import Queue
import sys
import re
import argparse
from subprocess import PIPE,Popen

headers={
    'Host': 'www.xicidaili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWI3Nzg0YTYwNmMzYjgzMWVhYzU0MjBlYTg2ZTJmN2VlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVBUVzdkOEdONGV6dmc1TjRkSUJsQk8vUWtYWTlMNUZ2Q2tFRzdtOXhwZGc9BjsARg%3D%3D--8a2737e5726fb3b0fb7c839c057a6ad6a1ef7fc2; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1587977250; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1587977835',
    'If-None-Match': 'W/"6579cc71c4d7159dfefe7f3197f9a2e2"'
}

def get_arg():
    parser=argparse.ArgumentParser()
    #print '-nn '
    parser.add_argument('-c',default='nn',dest='nn')
    args=parser.parse_args()
    return args

class Proxy_ip(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue=queue

    def run(self):
        while not self._queue.empty():
            url=self._queue.get()
            try:
                self.Spider(url)
            except Exception,e:
                print e
                pass

    def Spider(self,url):
        #print url
        html = requests.get(url=url, headers=headers)
        ip = re.findall('<td>(.*?)</td>', html.content)
        for i in range(0, 500, 5):
            #print ip[i] + ':' + ip[i + 1]
            f1=open('proxy_ip.txt','a+')
            f1.write(ip[i] + ':' + ip[i + 1]+'\n')
            f1.close()
            using(ip[i],ip[i+1])

def using(ip,port):
    check_ip=('telnet'+' '+'%s'+' '+'%s') %(ip,port)
    check_ip_new=check_ip.replace('\"','')
    use=Popen([check_ip_new],stdin=PIPE,stdout=PIPE,shell=True)
    using_ip=use.stdout.read()
    if using_ip:
        print using_ip+'open'
    else:
        print using_ip+'close'

def main():
    args=get_arg()
    if len(sys.argv)==1:
        print 'usage:'
        print '-c nn 采集国内高匿代理IP'
        print '-c nt 采集国内透明代理IP'
        print '-c wn 采集HTTPS代理IP'
        print '-c wt 采集HTTP代理IP'
        print '-c qq 采集SOCKS IP代理'
        exit(-1)
    else:
        queue=Queue.Queue()
        for i in range(1,3):
            #print args.nn
            queue.put('https://www.xicidaili.com/'+args.nn+'/'+ str(i))
        threads=[]
        thread_count=4
        for i in range(thread_count):
            threads.append(Proxy_ip(queue))
        for i in threads:
            i.start()
        for i in threads:
            i.join()

if __name__ == '__main__':
    main()






