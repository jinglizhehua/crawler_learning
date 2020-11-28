import flask
import os

app = flask.Flask(__name__)

# @app.route('/')
# def hello():
#     return '你好'

# @app.route('/')
# def index1():
#     try:
#         fobj = open('index.htm', 'rb')
#         data = fobj.read()
#         fobj.close()
#         return data
#     except Exception as err:
#         return str(err)

@app.route('/hi')
def hi():
    return 'Hi, 你好'

''' 服务器获取GET发送的数据 '''
# 用flask.request.args.get(参数)来获取参数的值
# @app.route('/')
# def index():
#     try:
#         # province = flask.request.args.get('province')
#         # city = flask.request.args.get('city')
#         # 此时客户端如果不提供参数会出现错误，改进：
#         province_get = flask.request.args.get('province') if 'province' in flask.request.args else ''
#         city_get = flask.request.args.get('city') if 'city' in flask.request.args else ''
#         return 'GET:' + province_get + city_get
#     except Exception as err:
#         print(err)

''' 服务器获取POST数据 '''
# flask.request.form.get(参数)
# 同时获取get和post：flask.request.values.get()
# @app.route('/', methods=['POST'])
# def index():
#     try:
#         province_post = flask.request.form.get('province') if 'province' in flask.request.form else ''
#         city_post = flask.request.form.get('city') if 'city' in flask.request.form else ''
#         return 'POST:' + province_post + city_post
#     except Exception as err:
#         print(err)

''' Web下载文件 '''
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'fileName' not in flask.request.values:
        return 'bird.jpg'
    else:
        data = b''
        try:
            fileName = flask.request.values.get('fileName')
            if fileName != '' and os.path.exists(fileName):
                fobj = open(fileName, 'rb')
                data = fobj.read()
                fobj.close()
        except Exception as err:
            print(err)
        return data
''' Web上传文件 '''
@app.route('/upload', methods=['POST'])
def upload_file():
    msg = ''
    try:
        if 'fileName' in flask.request.values:
            fileName = flask.request.values.get('fileName')
            data = flask.request.get_data()     # 读取二进制数据
            with open('upload' + fileName, 'wb') as fobj:
                fobj.write(data)
                fobj.close()
                msg = 'OK'
        else:
            msg = '没有按要求上传文件'
    except Exception as err:
        msg = str(err)
    return msg





if __name__ == '__main__':
    app.run()


