import requests
import json
import time
import datetime
from db import get_db_conn, close_db_conn

headers = {
    'cookie': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
db_file = 'histories.db'

def read_data_from_tags(_tags, _last):
    """
    _tags：需要获取数据的标签
    _last：存储已经保存的数据，用于判断新数据是否重复
    返回：新数据元组列表，是否没有重复数据
    """
    tag_list = []
    base_time = datetime.datetime.strptime('1970-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')
    for _item in _tags:
        cover = _item['cover']                       # 封面
        title = _item['title']                       # 标题
        uri   = _item['uri']                         # 直播房间网址
        bvid  = _item['history']['bvid']             # bv号
        page  = _item['history']['page']             # 第几p
        part  = _item['history']['part']             # 当前p的标题
        business  = _item['badge']                   # 视频类型
        videos = _item['videos']                     # 共几p
        author_name = _item['author_name']           # up主
        author_mid  = _item['author_mid']            # up主id
        view_at = str(base_time + datetime.timedelta(seconds=int(_item['view_at'])))     # 观看时间（秒）
        if int(_item['progress']) == -1:
            progress = '已看完'
        else:
            progress = str(datetime.timedelta(seconds=int(_item['progress'])))        # 看到第几秒了（-1表示看完）
        duration    = str(datetime.timedelta(seconds=int(_item['duration'])))            # 视频时间总长
        _tmp = (view_at, title, bvid, author_name, author_mid, page, part, videos, progress, duration, cover, business, uri)
        if _tmp in _last:
            return tag_list, False
        print(title)
        tag_list.append(_tmp)
    return tag_list, True

def get_history(_last):
    """
    _last：已经保存的数据，用于判断新数据是否重复
    返回：所有新数据（顺序从新到旧）
    """
    saves = []
    url = 'https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business='
    print('获取历史记录...')
    run_flag = True
    while run_flag:
        time.sleep(1)

        html = requests.get(url=url, headers=headers).text
        js = json.loads(html)           # str 转 json
        tags = js['data']['list']
        if len(tags) == 0:
            break

        tmp, run_flag = read_data_from_tags(tags, _last)
        saves += tmp

        max_ = tags[-1]['view_at']
        view_at = tags[-1]['view_at']
        url = 'https://api.bilibili.com/x/web-interface/history/cursor?max=' + str(max_) + '&view_at=' + str(view_at) + '&business=archive'
    return saves

def read_last_data():
    conn = get_db_conn(db_file)
    cur = conn.cursor()
    sql = 'select 观看时间, 标题, bv号, up, up_id, 看到第几p, 当前p标题, 共几p, 已观看时间, 视频总时长, 封面, 类型, 相关网址 ' \
          'from history'
    cur.execute(sql)
    tmp = cur.fetchall()
    close_db_conn(cur, conn)
    return tmp

def write_to_file(saves):
    print('获取完成，开始写入文件...')
    conn = get_db_conn(db_file)
    cur = conn.cursor()
    sql = 'insert into history ' \
          '(观看时间, 标题, bv号, up, up_id, 看到第几p, 当前p标题, 共几p, 已观看时间, 视频总时长, 封面, 类型, 相关网址) ' \
          'values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    while len(saves) != 0:
        tmp = saves.pop()
        cur.execute(sql, tmp)
    print('写入完成，开始保存文件...')
    conn.commit()
    close_db_conn(cur, conn)
    print('文件已保存，程序运行结束.')

if __name__ == '__main__':
    last = read_last_data()  # 用于判断上次读取位置
    histories = get_history(last)
    write_to_file(histories)


