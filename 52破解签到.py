import requests
from bs4 import BeautifulSoup
import os
import json
# 调取需要的模块
url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
with open('cookie_52pojie.txt', 'r') as file:
    cookies = file.read()
    cookies = json.loads(cookies)
    file.close()

sess = requests.session()
sess.headers = headers
for cookie in cookies:
    sess.cookies.set(cookie['name'], cookie['value'])
    # print(cookie['name'], cookie['value'])

html = sess.get(url=url).text
b = BeautifulSoup(html, 'lxml')
# 下面就是签到之后返回的结果，如果成功则返回成功，如果已经签到过就会提示不是在进行的任务，cookie不对则提示没有登录
c = b.find('div', id='messagetext').find('p').text
print(c)
