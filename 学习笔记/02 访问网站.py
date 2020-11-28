import urllib.request
import urllib.parse
import os

''' Urllib访问web网站 '''
def urllib_run():
    url = 'http://127.0.0.1:5000'
    try:
        html = urllib.request.urlopen(url).read().decode()
        print(html)
    except Exception as err:
        print(err)
''' GET方法访问网站 '''
# 客户端GET方式发送数据
# 数据附加在url后面， url?名称1=值1&名称2=值2&……
# 如果值包含汉字，要用urllib.parse.quote进行编码
def get_send():
    url = 'http://127.0.0.1:5000'
    try:
        province = urllib.parse.quote('广东')
        city = urllib.parse.quote('深圳')
        data = 'province=' + province + '&city=' + city
        html = urllib.request.urlopen(url + '?' + data).read().decode()
        print(html)
    except Exception as err:
        print(err)
''' POST方法向网站发送数据 '''
# 客户端向房务段发送表单数据，结构为："名称1=值1&名称2=值2&……"
def post_send():
    url = 'http://127.0.0.1:5000'
    try:
        # 方法一
        province = urllib.parse.quote('广东')
        city = urllib.parse.quote('深圳')
        data1 = ('province=' + province + '&city=' + city).encode()  # 按UTF-8编码转换为二进制数据
        # 方法二
        data2 = urllib.parse.urlencode({'name': 'nihahaha', 'pass': 'hahdsoifho'}).encode('utf-8')

        # 方法一
        # html = urllib.request.Request('https://www.iqianyue.com/mypost', data=data2)
        # html = urllib.request.urlopen(html).read().decode()
        # 方法二
        html = urllib.request.urlopen('http://127.0.0.1:5000', data=data1).read().decode()   # data参数必须是二进制
        print(html)
    except Exception as err:
        print(err)
''' Web下载文件 '''
def web_download():
    url = 'http://127.0.0.1:5000'
    try:
        fileName = urllib.request.urlopen(url).read().decode()
        print('准备下载：' + fileName)
        data = urllib.request.urlopen(url + '?fileName=' + fileName).read()
        fobj = open('download' + fileName, 'wb')
        fobj.write(data)
        fobj.close()
        print('下载完毕：', len(data), '字节')
    except Exception as err:
        print(err)
''' Web上传文件 '''
def web_upload():
    url = 'http://127.0.0.1:5000/upload'
    # fileName = input('Enter the file:')
    fileName = 'bird.jpg'
    if os.path.exists(fileName):
        fobj = open(fileName, 'rb')
        print(fobj)
        data = fobj.read()
        fobj.close()
        print('准备上传：' + fileName)

        headers = {'content-type': 'application/octet-stream'}
        purl = url + '?fileName=' + urllib.parse.quote(fileName)
        req = urllib.request.Request(purl, data=data, headers=headers)
        msg = urllib.request.urlopen(req).read().decode()
        if msg == 'OK':
            print('成功上传：', len(data), '字节')
        else:
            print(msg)
    else:
        print('文件不存在!')


if __name__ == '__main__':
    urllib_run()
    get_send()
    post_send()
    web_download()
    web_upload()


