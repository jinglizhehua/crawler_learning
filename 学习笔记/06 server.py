import flask
import os

app = flask.Flask(__name__)

def getFile(fileName):
    data = b""
    if os.path.exists('./htmls_graph/' + fileName):
        fobj = open('./htmls_graph/' + fileName, 'rb')
        data = fobj.read()
        fobj.close()
    return data

@app.route('/')
def index():
    return getFile('books.htm')

@app.route('/<section>')
def process(section):
    data = b""
    if section != "":
        data = getFile(section)
    return data

if __name__ == '__main__':
    app.run()
