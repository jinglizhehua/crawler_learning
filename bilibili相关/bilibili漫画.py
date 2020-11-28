import requests
from bs4 import BeautifulSoup
import json
import time
import os
import threading

headers = {
    'cookie': 'your cookies',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

retrytime = 30    # 重试时间(s)
outtime = 15      # 超时时间(s)
download_list = []

def download_img(ep_id, path, ordernum):
    global retrytime
    global outtime
    global download_list
    data = {
        # 'ep_id': '300318'
        'ep_id': ep_id
    }
    url = 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web'

    req = requests.post(url=url, headers=headers, data=data).json()
    for i, item in enumerate(req['data']['images']):
        # 判断文件是否已存在，若存在则当成已经下载过，不再下载
        if os.path.exists(path + '/img%02d.jpg' % i):
            continue
        time.sleep(0.5)
        print('下载 第[{}]话 第{}张图片...'.format(ordernum, i), end='\r')
        url = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web'
        data = {
            'urls': "[\"{}\"]".format(item['path'])
        }
        while True:
            try:
                resp = requests.post(url=url, headers=headers, data=data, timeout=outtime).json()['data'][0]
            except Exception as err:
                print(err)
            else:
                break
        url = resp['url'] + '?token=' + resp['token']
        # img = requests.get(url=url).content
        relink = True      # 重连标志
        while relink:
            try:
                relink = False
                img = requests.get(url=url, timeout=outtime).content
            except Exception as err:
                relink = True
                print('第[{}]话下载出错...                 '.format(ordernum))
                print(err)
                print('{}秒之后尝试重连...'.format(retrytime))
                time.sleep(retrytime)
            else:
                with open(path + '/img%02d.jpg' % i, 'wb') as img_file:
                    img_file.write(img)
                    img_file.close()
    print('* * * * * 第[{}]话下载完成 (共{}张图片)               '.format(ordernum, len(req['data']['images'])))
    download_list.remove(ordernum)
    print('- - - - - 剩余未下载：', download_list)

def get_index(comic_id, start=1, end=1):
    url = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web'
    data = {"comic_id": comic_id}
    post = requests.post(url=url, headers=headers, data=data).json()
    manhua_name = post['data']['title']
    if not os.path.exists('./download_manhua/' + manhua_name):
        os.mkdir('./download_manhua/' + manhua_name)

    print('# # # # # 开始下载漫画：' + manhua_name)
    post = post['data']['ep_list']
    post.sort(key=lambda x: x['ord'])
    for item in post[start-1:end]:
        if item['is_locked']:
            print('! ! ! ! ! 第[{}]话未解锁!'.format(item['ord']))
        else:
            print('^ ^ ^ ^ ^ 开始下载 [{}] {} {}'.format(item['ord'], item['short_title'], item['title']))
            ord_f = ''
            if type(item['ord']) == int:
                ord_f = '%03d' % item['ord']
            elif type(item['ord']) == float:
                ord_f = '%03.1f' % item['ord']
            mh_dir = './download_manhua/' + manhua_name + '/[ {} ] {} {}'.format(ord_f, item['short_title'], item['title']).rstrip()
            if not os.path.exists(mh_dir):
                os.mkdir(mh_dir)


            # download_img(item['id'], mh_dir, item['ord'])
            thread_tmp = threading.Thread(target=download_img, args=[item['id'], mh_dir, item['ord']])
            thread_tmp.setDaemon(False)     # 后台线程
            thread_tmp.start()
            download_list.append(item['ord'])


            # relink = True      # 重连标志
            # while relink:
            #     try:
            #         relink = False
            #         download_img(item['id'], mh_dir)
            #     except Exception as err:
            #         relink = True
            #         print(err)
            #         print('5秒之后尝试重连...')
            #         time.sleep(5)


def download_manhua():
    global retrytime
    global outtime
    comic_id = int(input('请输入bilibili漫画id:'))
    start = int(input('想从第几话开始下载:'))
    end = int(input('想下载到第几话:'))
    ot = input('设置超时时间(直接回车则默认为{}秒):'.format(outtime))
    if ot != '':
        outtime = int(ot)
    ot = input('设置重试时间(直接回车则默认为{}秒):'.format(retrytime))
    if ot != '':
        retrytime = int(ot)
    get_index(comic_id, start, end)

if __name__ == '__main__':
    download_manhua()

