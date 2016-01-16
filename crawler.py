# -*- coding:utf-8 -*-
#!/usr/bin/env python

import urllib2
import re
import urlparse
import os
import urllib
StandardTimeout = 10
from string import *
import threading
import Queue
import time
import HTMLParser


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def htmlStandardize(html):  #去除html转义字符
    try:
        htmlParser = HTMLParser.HTMLParser()
        return str(htmlParser.unescape(html))
    except:
        return html.replace('&amp;','&').replace('&gt;','>').replace('&lt;','<').replace('&quot;','\"').replace('&nbsp;',' ')

def judgeChinese(html):
    lang = re.search('lang=\"(.*?)\"', html, re.I)
    if lang == None or 'zh' in lang.group(1).lower():
        return True
    return False

def get_page(page):
#    content = ''
    try:
        content = urllib2.urlopen(page, timeout = StandardTimeout)
    except:
        #print "Timeout"
        pass
    return content

def get_all_links(content, page):
    links = []
    #print CompRule
    soup = CompRule.findall(htmlStandardize(content))
    #print soup
    for url in soup:
        url = urlparse.urljoin(page,url)
        if url not in links and not url==page:
            links.append(url)
    return links

def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'pre-index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'html_folder'                 #存放网页的文件夹
    filename = valid_filename(page) #将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)                #将网页存入文件
    f.close()

#----------------------------------------#

def working(q, crawled, graph, max_page):
    global count
    while True:
        page = q.get()  #得到q队列中顶端的url
        if (page == '' or count >= max_page):
            break
        #print type(crawled)
        try:
            c = get_page(page)      #得到该url的内容
            origin = c.geturl()       #将网页内容还原为原始url
            if origin not in crawled:
                #print page.decode('UTF8')
                #if (count%500==0):
                #    print 'Crawling...', float(count)/max_page*100, '%'
                content = c.read()
                if judgeChinese(content):
                    add_page_to_folder(page, content)
                    count += 1
                    outlinks = get_all_links(content, page)
                    #globals()['union_%s' % method](tocrawl, outlinks)
                    for link in outlinks:
                        q.put(link)
                    if varlock.acquire():
                        graph[page] = outlinks
                        crawled.append(origin)
                        varlock.release()
                    q.task_done()
        except:
            pass
    while q.qsize():             #当抓取页面数达到要求之后，需要清空队列中的项
        try:
            q.task_done()
        except:
            pass

def crawl(seed, max_page):
    start = time.clock()
    varlock = threading.Lock()
    q = Queue.Queue()
    q.put(seed)
    THREAD_NUM = 100#max_parrel
    crawled = []
    graph = {}
    global count
    count = 0
    for i in range(THREAD_NUM):
        t = threading.Thread(target=working, args=(q, crawled, graph, max_page))
        t.setDaemon(True)
        t.start()
    q.join()
    return graph, crawled, time.clock()-start

if __name__ == '__main__' :
    CompRule = re.compile('a .*?href=\"((?:http|\/).+?)\"', re.I)
    ##graph, crawled = dfs('http://www.udacity.com/cs101x/urank/index.html')
    #seedlib = ['http://www.baidu.com', 'http://www.renren.com', 'http://www.sohu.com/', 'http://www.taobao.com', 'http://www.xinhuanet.com', 'http://www.ifeng.com']
    seedlib = ['http://www.jd.com']
    for WebAddress in seedlib:
        graph, crawled, time_needed = crawl(WebAddress, 10000)
        #print 'next website'

    print 'Total: '+str(count)
    print 'Crawl..Time cost: '+str(time_needed)
else:
    pass


