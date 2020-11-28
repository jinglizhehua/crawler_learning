from bs4 import BeautifulSoup
import urllib.request

start_url = 'http://127.0.0.1:5000'

mark1 = []
''' 递归 '''
def spider_digui(url):
    global mark1
    if url not in mark1:
        try:
            data = urllib.request.urlopen(url).read().decode()
            soup = BeautifulSoup(data, 'lxml')
            print(soup.find('h3').text)
            mark1.append(url)
            items = soup.select('a[href]')
            for item in items:
                spider_digui(start_url + '/' + item['href'])
        except Exception as err:
            print(err)
# spider_digui(start_url)

''' 深度优先 '''
class Stack:
    def __init__(self):
        self.st = []
    def pop(self):
        return self.st.pop()
    def push(self, obj):
        self.st.append(obj)
    def empty(self):
        return len(self.st) == 0
mark2 = []
def spider_shendu(url):
    global mark2
    st = Stack()
    st.push(url)
    while not st.empty():
        tmp = st.pop()
        if tmp not in mark2:
            mark2.append(tmp)
            try:
                data = urllib.request.urlopen(tmp).read().decode()
                soup = BeautifulSoup(data, 'lxml')
                print(soup.find('h3').text)
                items = soup.select('a[href]')
                for item in items[::-1]:
                    st.push(start_url + '/' + item['href'])
            except Exception as err:
                print(err)
# spider_shendu(start_url)

''' 广度 '''
class Queue:
    def __init__(self):
        self.qu = []
    def fetch(self):
        return self.qu.pop(0)
    def enter(self, obj):
        self.qu.append(obj)
    def empty(self):
        return len(self.qu) == 0
mark3 = []
def spider_guangdu(url):
    global mark3
    qu = Queue()
    qu.enter(url)
    while not qu.empty():
        tmp = qu.fetch()
        if tmp not in mark3:
            mark3.append(tmp)
            try:
                data = urllib.request.urlopen(tmp).read().decode()
                soup = BeautifulSoup(data, 'lxml')
                print(soup.find('h3').text)
                items = soup.select('a[href]')
                for item in items:
                    qu.enter(start_url + '/' + item['href'])
            except Exception as err:
                print(err)
spider_guangdu(start_url)



