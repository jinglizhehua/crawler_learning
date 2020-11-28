from bs4 import BeautifulSoup
import urllib.request
import gzip
import json
import time
import openpyxl
import datetime

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'your cookies',
    'referer': 'https://www.bilibili.com/account/history',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

url  = 'https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business='

# bus = {'archive': '视频', 'live': '直播', 'article': '专栏', 'pgc': '番剧'}
base_time = datetime.datetime.strptime('1970-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')
row_num = 13    # 存储列数
col_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

saves = []
wb = openpyxl.load_workbook('历史记录.xlsx')   # 打开工作簿
sh = wb['Sheet1']
last = []       # 用于判断上次读取位置
widths = [sh.column_dimensions[col_list[i]].width for i in range(row_num)]     # 读取原列宽
for tmp in list(sh.rows)[1:]:
    _tmp = []
    for i in range(row_num):
        if tmp[i].value is None:
            _tmp.append("")
        else:
            _tmp.append(tmp[i].value)
    last.append(_tmp)

print('获取历史记录...')
run_flag = True
while run_flag:
    time.sleep(1)

    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    try:
        html = gzip.decompress(html).decode()
    except Exception as err:
        print(err)
        html = html.decode()
    js = json.loads(html)           # str 转 json
    tags = js['data']['list']
    if len(tags) == 0:
        break

    for item in tags:
        cover = item['cover']                       # 封面
        title = item['title']                       # 标题
        uri   = item['uri']                         # 直播房间网址
        bvid  = item['history']['bvid']             # bv号
        page  = item['history']['page']             # 第几p
        part  = item['history']['part']             # 当前p的标题
        business  = item['badge']                   # 视频类型
        videos = item['videos']                     # 共几p
        author_name = item['author_name']           # up主
        author_mid  = item['author_mid']            # up主id
        view_at = str(base_time + datetime.timedelta(seconds=int(item['view_at'])))     # 观看时间（秒）
        if int(item['progress']) == -1:
            progress = '已看完'
        else:
            progress = str(datetime.timedelta(seconds=int(item['progress'])))        # 看到第几秒了（-1表示看完）
        duration    = str(datetime.timedelta(seconds=int(item['duration'])))            # 视频时间总长
        tmp = [view_at, title, bvid, author_name, author_mid, page, part, videos, progress, duration, cover, business, uri]
        if tmp in last:
            run_flag = False
            break
        print(item['title'])
        saves.append(tmp)

    max_ = tags[-1]['view_at']
    view_at = tags[-1]['view_at']
    url = 'https://api.bilibili.com/x/web-interface/history/cursor?max=' + str(max_) + '&view_at=' + str(view_at) + '&business=archive'

print('获取完成，开始写入文件...')
while len(saves) != 0:
    tmp = saves.pop()
    _row = len(list(sh.rows)) + 1  # 获取行数
    for i in range(row_num):
        sh.cell(row=_row, column=i+1, value=tmp[i])
for i in range(row_num):
    sh.column_dimensions[col_list[i]].width = widths[i]
print('写入完成，开始保存文件...')
save_flag = True
while save_flag:
    save_flag = False
    try:
        wb.save('历史记录.xlsx')
    except Exception as err:
        print(err)
        print('请关闭Excel !!!')
        time.sleep(1)
        save_flag = True
print('文件已保存，程序运行结束.')

'''
用*判断是否相同
{
cover : 封面
`title    : 标题
uri : 直播房间网址，其他为""
history:{`bvid: bv号*      `page: 第几p       `part: 第几p的标题     business: 类型(archive视频 live直播 article专栏)}
`videos: 共几p
`author_name: up主
`author_mid : up主id
badge: 类型
`view_at: 观看时间(秒)*
`progress: 看到第几秒了(-1表示看完了)
`duration: 总长时间
}
'''

