#coding=utf-8
import requests
import Queue
import threading
import argparse
import sys
import os

class dirscan(threading.Thread):
    def __init__(self,queue,remove,output):
        threading.Thread.__init__(self)
        self._queue=queue
        self.remove = remove
        self.output = output

    def run(self):
        while not self._queue.empty():
            url=self._queue.get()
            try:
                scan(url,self.remove,self.output)
            except Exception,e:
                print e
                pass

def scan(url,remove,output):
    requests.packages.urllib3.disable_warnings()
    html=requests.get(url=url,timeout=4,verify=False)
    if html.status_code == int(remove):
        print remove +'  '+  url
        output_file(url,output,remove)
    else:
        pass
def output_file(url,output,remove):
    with open(output,'a+') as f:
        f.write(remove + ' ' +url)

def domain_url(domain_file):
    url=[]
    with open(domain_file, 'r') as urls:
        for url in urls.readlines():
            print url
            #url.append(url)
    return url
def main():
    queue=Queue.Queue()
    parser = argparse.ArgumentParser(description='dir scan')
    parser.add_argument('-u','--url', dest='url',help='scan url')
    parser.add_argument('-d', '--domain', dest='domain_file', help='domain_file')
    parser.add_argument('-f','--file', dest='file', help='file')
    parser.add_argument('-t', '--threads', dest='threads',default=10, help='scan threads')
    parser.add_argument('-r', '--remove', dest='remove', help='remove status code')
    parser.add_argument('-o', '--output', dest='output',help='output file')
    args = parser.parse_args()
    remove=args.remove
    output=args.output
    try:
        if args.url:
            url = 'http://' + args.url
        else:
            domain_url(args.domain_file)
    except Exception,e:
        print e
        exit(1)
    print '1111'
    print url
    if os.path.exists(output):
        os.remove(output)
    with open(args.file,'r') as f:
        for f_content in f.readlines():
            queue.put(url+f_content)
    threads=[]
    thread_count=int(args.threads)
    print thread_count
    for i in range(thread_count):
        threads.append(dirscan(queue,remove,output))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    main()









