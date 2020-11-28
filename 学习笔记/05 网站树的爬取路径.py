from bs4 import BeautifulSoup
import urllib.request

r'''
网页结构：
                    计算机
            /         |         \
         数据库      程序设计       计算机网络
      /             |       \
    /              |         \
MySQL数据库    Python程序设计   Java程序设计
'''

start_url = 'http://127.0.0.1:5000'

''' 递归程序爬取数据 '''
def spider_digui(url):
    try:
        data = urllib.request.urlopen(url).read().decode()
        soup = BeautifulSoup(data, 'lxml')
        print(soup.find('h3').text)
        links = soup.select('a')
        for link in links:
            url = start_url + '/' + link['href']
            spider_digui(url)
    except Exception as err:
        print(err)
# spider_digui(start_url)

''' 深度优先爬取数据 '''
class Stack:
    def __init__(self):
        self.st = []
    def pop(self):
        return self.st.pop()
    def push(self, obj):
        self.st.append(obj)
    def empty(self):
        return len(self.st) == 0
# 1. 第一个url入栈
# 2. 如果栈为空则程序结束，否则出栈一个url，爬取它的<h3>
# 3. 获取url的所有<a>的href值，把这些值压栈
def spider_shendu(url):
    st = Stack()
    st.push(url)
    while not st.empty():
        tmp = st.pop()
        try:
            data = urllib.request.urlopen(tmp).read().decode()
            soup = BeautifulSoup(data, 'lxml')
            print(soup.find('h3').text)
            items = soup.select('a[href]')
            for item in items[::-1]:      # 倒序
                st.push(url + '/' + item['href'])
        except Exception as err:
            print(err)
# spider_shendu(start_url)

''' 广度优先爬取数据 '''
class Queue:
    def __init__(self):
        self.qu = []
    def fetch(self):
        return self.qu.pop(0)
    def enter(self, obj):
        self.qu.append(obj)
    def empty(self):
        return len(self.qu) == 0
# 1. 第一个url入列
# 2. 如果列空则程序结束，否则出列一个url，爬取它的<h3>
# 3. 获取url的所有<a>的href值，这些值全部入列
def spider_guangdu(url):
    qu = Queue()
    qu.enter(url)
    while not qu.empty():
        try:
            tmp = qu.fetch()
            data = urllib.request.urlopen(tmp)
            soup = BeautifulSoup(data, 'lxml')
            print(soup.find('h3').text)
            items = soup.select('a[href]')
            for item in items:
                qu.enter(url + '/' + item['href'])
        except Exception as err:
            print(err)
spider_guangdu(start_url)




