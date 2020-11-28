import requests
from bs4 import BeautifulSoup

url = 'http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Cookie': 'your cookies'
}
data = {
    'formhash': '6cbcb8ea',
    'qdxq': 'kx',
    'qdmode': 1,
    'todaysay': '新的一天，新的开始~~~~',
    'fastreply': 0
}

html = requests.post(url=url, data=data, headers=headers).text
soup = BeautifulSoup(html, 'lxml')
# print(html)
print(soup.select('div[class="c"]')[0].text.replace('\n', ''))

