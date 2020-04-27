# 利用队列和多线程对犯贱网进行爬取
from queue import Queue
import threading
import time
import requests
from lxml import etree
import json

# 列表用来存放采集线程
g_crawl_list=[]
# 列表用来存放采集线程
g_parse_list=[]

class CrawlThread(threading.Thread):
    def __init__(self , name , page_queue , data_queue):
        super(CrawlThread,self).__init__()
        self.name=name
        self.data_queue=data_queue
        self.page_queue=page_queue
        self.url='http://www.ifanjian.net/jianwen-{}'
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
    def run(self):
        print('%s---线程启动---'%self.name)
        while 1:#让线程一直跑
            #采集线程
            if self.page_queue.empty():
                break
            #从队列中取出页码
            #拼接url发送请求
            #响应内容放入data_queue中
            page=self.page_queue.get()
            url=self.url.format(page)
            r=requests.get(url,headers=self.headers)
            self.data_queue.put(r.text)
        print('%s---线程结束---' % self.name)

class ParseThread(threading.Thread):
    def __init__(self,name,data_queue,fp,lock):
        super(ParseThread,self).__init__()
        self.name = name
        self.data_queue = data_queue
        self.fp=fp
        self.lock=lock
    def run(self):
        print('%s---线程启动---'%self.name)
        while 1:
            data=self.data_queue.get(True,5)
            self.parse_content(data)
        print('%s---线程结束---' % self.name)

    def parse_content(self,data):

        tree=etree.HTML(data)
        items = []
        title=tree.xpath('//h2[@class="cont-list-title"]/a/text()')
        content=tree.xpath('//li[@class="cont-item"]//p/img/@data-src')
        for j in range(len(content)):
            item={
                '标题':title[j],
                '图片链接':content[j]
                }
            items.append(item)
        self.lock.acquire()
        self.fp.write(json.dumps(items,ensure_ascii=False)+'\n')
        self.lock.release()


def create_crawl_thread(page_queue,data_queue):
    crawl_name=['采集线程1号','采集线程2号','采集线程3号']
    for name in crawl_name:
        tcrawl = CrawlThread(name,page_queue,data_queue)
        g_crawl_list.append(tcrawl)

def create_parse_thread(data_queue,fp,lock):
    parse_name = ['解析线程1号', '解析线程2号', '解析线程3号']
    for name in parse_name:
        tparse = ParseThread(name,data_queue,fp,lock)
        g_parse_list.append(tparse)

def create_queue():
    # 创建页码队列
    page_queue = Queue()
    for page in range(1,11):#11页
        page_queue.put(page)
    # 创建内容队列
    data_queue = Queue()
    return page_queue,data_queue


def main():
    #创建队列
    page_queue,data_queue=create_queue()
    fp=open('jian.json','a',encoding='utf-8')
    lock=threading.Lock()
    #创建采集线程
    create_crawl_thread(page_queue,data_queue)
    time.sleep(3)
    #创建解析线程
    create_parse_thread(data_queue,fp,lock)

    #启动所有采集线程
    for tcrawl in g_crawl_list:
        tcrawl.start()
    #启动所有解析线程
    for tparse in g_parse_list:
        tparse.start()

    #主线程等待子线程结束
    for tcrawl in g_crawl_list:
        tcrawl.join()
    for tparse in g_parse_list:
        tparse.join()
    fp.close()
    print('主线程子线程都结束')

if __name__ == '__main__':
    main()