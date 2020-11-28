from urllib import request
import requests
from bs4 import BeautifulSoup
import random
import time

url = 'http://tieba.baidu.com/f/like/mylike?v=1598242961773'
headers = {
    'Cookie': 'your cookies',
    'Host': 'tieba.baidu.com',
    'Referer': 'http://tieba.baidu.com/i/i/forum',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

req = request.Request(url=url, headers=headers)
html = request.urlopen(req).read().decode('gbk')
soup = BeautifulSoup(html, 'lxml')

div = soup.select('body div div')[-1]
items = div.select('a')
urls = [url]
for item in items[:-2]:
    urls.append('http://tieba.baidu.com' + item['href'])

titles = []
print('获取关注列表...')
for url in urls:
    time.sleep(2)
    try:
        req = request.Request(url=url, headers=headers)
        html = request.urlopen(req).read().decode('gbk')
        soup = BeautifulSoup(html, 'lxml')

        for item in soup.select('table tr')[1:]:
            titles.append(item.find('td').find('a')['title'])
    except Exception as err:
        print(err)
print('开始签到...')

url = 'https://tieba.baidu.com/sign/add'
headers = {
    'Cookie': r'BIDUPSID=8D7C2164B5855A25CE6E1101CE6F3C3B; PSTM=1592472833; TIEBA_USERTYPE=23d7f1bb2cb245e58ae89739; bdshare_firstime=1592485974718; TIEBAUID=e00402780b9907c77439aa0a; H_WISE_SIDS=148078_145790_147939_148226_149984_150073_147091_150085_148193_148867_150799_150914_150744_147280_150036_149587_149540_151017_148754_147897_146575_148524_127969_151297_146548_150558_149718_146732_138425_149557_151117_151227_131423_144659_147527_145597_107317_150590_148186_147717_149253_151171_150780_146396_144966_139882_150340_151188_147546_148868_110085; rpln_guide=1; IS_NEW_USER=df77991d5b432a85d8a2f832; CLIENTWIDTH=738; CLIENTHEIGHT=1550; SEENKW=%E5%A4%A9%E5%A0%82%E5%B7%B4%E6%AF%94%E4%BC%A6%23%E4%BA%BA%E7%B1%BB%E4%B8%80%E8%B4%A5%E6%B6%82%E5%9C%B0; MCITY=-%3A; BAIDUID=3E2CE5941DA38B2F071F8A9B1194E156:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=3E2CE5941DA38B2F071F8A9B1194E156:FG=1; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1605604796,1605619828,1605714881,1605847508; BA_HECTOR=8121ah010k002ka16v1frekmm0r; BDUSS=ENhYVhrMHc1MzBOSTd4TmkycGp2VGxBNTdrVW9XWTlWdDI5RTNpVUF3eno0ZDVmRVFBQUFBJCQAAAAAAAAAAAEAAABz26AYbWl3ZW5qaWUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPNUt1~zVLdfb; BDUSS_BFESS=ENhYVhrMHc1MzBOSTd4TmkycGp2VGxBNTdrVW9XWTlWdDI5RTNpVUF3eno0ZDVmRVFBQUFBJCQAAAAAAAAAAAEAAABz26AYbWl3ZW5qaWUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPNUt1~zVLdfb; H_PS_PSSID=32810_1423_33103_33058_31253_33098_33101_32961_31709; STOKEN=34951b2b664b41309245c0fbc8ef469e7881cc721996312f41cc09d76e767c87; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1605714662,1605714881,1605847508,1605850739; st_key_id=17; showCardBeforeSign=1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1605850800; st_data=a868152d0e3c0b9990e62fb8fe89ecea36d6f6df2e7984b5cb5eac112cd727bc65b4f83405aefe95f1cc1f0b9e0615785e1d266ac4c67072ce97b49948d9e24358518facc8d6fb47110929ea4576cdae0aa99d4890f7ef8c68f2f537b60110c3b7cc48661262b72026642d05112726a50d3a68a20ac6a09787e19a2c36118ed034334b5e4023910eb3e97f86cd00f78b; st_sign=39f6086d',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}
for title in titles:
    # time.sleep(random.random())
    try:
        ol = len(title.encode('GBK')) - len(title)
        print('{:<{out_len}}'.format(title, out_len=20-ol), end='')
    except Exception as err:
        print('{:<20}'.format(title), end='')
        print(err)
    data = {
        'ie': 'utf-8',
        'kw': title,
        'tbs': '4b8a5bf2a5363d1d1605850799'
    }
    try:
        response = requests.post(url=url, data=data, headers=headers)
        html = response.json()
        tmp = html['error']
        if tmp == '':
            tmp = html['data']['errmsg']
        if tmp == 'success':
            print(tmp, end='\r')
        else:
            print(tmp)
    except Exception as err:
        print(err)

print('签到完成')

