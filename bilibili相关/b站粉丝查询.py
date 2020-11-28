import time
import os
import requests
import json
from bs4 import BeautifulSoup

with open('./fans/last_date.txt', 'r') as date_file:
    last = date_file.readline()
    date_file.close()
date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())

uids = dict()  # {id: name}
new_fan = []        # 新增
lost_fan = []       # 取关
change_fan = []     # 改名
if last != '':
    with open('./fans/' + last + '.txt', 'r', encoding='utf-8') as file:
        for tmp in file.readlines():
            tmp = tmp.replace('\n', '')
            if tmp == '***新增***':
                break
            t = tmp.split(': ')
            uids[t[0]] = t[1]

url = 'https://api.bilibili.com/x/relation/followers'
headers = {
    'cookie': 'your cookies',
    'referer': 'https://space.bilibili.com/用户id/fans/fans',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
params = {
    'vmid': '填用户id',
    'pn': '1',
    'ps': '20',
    'order': 'desc',
    'jsonp': 'jsonp',
    'callback': '__jp5'
}

try:
    i = 1
    reads = dict()
    with open('./fans/' + date + '.txt', 'w', encoding='utf-8') as file:
        print('获取当前粉丝列表...')
        while True:
            time.sleep(0.5)
            params['pn'] = str(i)
            i += 1
            html = requests.get(url=url, headers=headers, params=params).text
            html = html.replace('__jp5(', '')
            html = html.replace(')', '')
            read = json.loads(html)
            if len(read['data']['list']) == 0:
                break
            print('读取第{}页'.format(i-1), end='\r')
            for item in read['data']['list']:
                mid, uname = str(item['mid']), item['uname']
                l_tmp = [mid, uname]
                file.write(mid + ': ' + uname + '\n')
                if mid in uids:
                    if uname != uids[mid]:                  # 改名
                        change_fan.append(l_tmp)
                    del uids[mid]
                else:                                       # 新增
                    new_fan.append(l_tmp)
        print('获取完成.')
        for item in uids.keys():                            # 取关
            lost_fan.append([item, uids[item]])

        file.write('***新增***\n')
        print('新增：')
        for item in new_fan:
            file.write(item[0] + ': ' + item[1] + '\n')
            print(item[0] + ': ' + item[1])
        file.write('***取关***\n')
        print('取关：')
        for item in lost_fan:
            file.write(item[0] + ': ' + item[1] + '\n')
            print(item[0] + ': ' + item[1])
        file.write('***改名***\n')
        print('改名：')
        for item in change_fan:
            file.write(item[0] + ': ' + item[1] + '\n')
            print(item[0] + ': ' + item[1])

        file.close()
except Exception as err:
    print('出错了！')
    print(err)
    os.remove('./fans/' + date + '.txt')
else:
    if len(new_fan) + len(lost_fan) + len(change_fan) > 0:
        with open('./fans/last_date.txt', 'w') as date_file:
            date_file.write(date)
            date_file.close()
    else:
        print('粉丝没有变动...')
        os.remove('./fans/' + date + '.txt')

print('完成')

