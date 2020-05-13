#coding=utf-8
import requests
import Queue
import threading
import argparse
import sys
import os
import User_agent

class dirscan(threading.Thread):
    def __init__(self,queue,status_code,output):
        threading.Thread.__init__(self)
        self._queue=queue
        self.status_code = status_code
        self.output = output

    def run(self):
        while not self._queue.empty():
            url=self._queue.get()
            try:
                scan(url,self.status_code,self.output)
            except Exception,e:
                print e
                pass

def scan(url,status_code,output):
    requests.packages.urllib3.disable_warnings()
    html=requests.get(url=url,timeout=4,verify=False,User_agent=User_agent.random_agent())
    if html.status_code == int(status_code):
        print status_code +'  '+  url
        output_file(url,output,status_code)
    else:
        pass
def output_file(url,output,status_code):
    with open(output,'a+') as f:
        f.write(status_code + ' ' +url+'\n')

def main():
    queue=Queue.Queue()
    parser = argparse.ArgumentParser(description='dir scan')
    parser.add_argument('-u','--url', dest='url',help='scan url')
    parser.add_argument('-d', '--domain', dest='domain_file', help='domain_file')
    parser.add_argument('-f','--file', dest='file', help='file')
    parser.add_argument('-t', '--threads', dest='threads',default=30, help='scan threads')
    parser.add_argument('-s', '--status_code', dest='status_code', help='target status_code')
    parser.add_argument('-o', '--output', dest='output',help='output file')
    args = parser.parse_args()
    status_code=args.status_code
    output=args.output
    try:
        if args.url:
            url = args.url
            with open(args.file, 'r') as f:
                for f_content in f.readlines():
                    queue.put(url + f_content)
        else:
            with open(args.domain_file, 'r') as urls:
                for url in urls.readlines():
                    url=url.strip()
                    print url
                    with open(args.file, 'r') as f:
                        for f_content in f.readlines():
                            queue.put(url + f_content.strip())
    except Exception,e:
        print e
        exit(1)
    if os.path.exists(output):
        os.remove(output)
    threads=[]
    thread_count=int(args.threads)
    print thread_count
    for i in range(thread_count):
        threads.append(dirscan(queue,status_code,output))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    main()









