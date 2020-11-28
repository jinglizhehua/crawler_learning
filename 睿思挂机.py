import time
import requests
from bs4 import BeautifulSoup
import re
 
 
def ruisi():
    url = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=330426&do=profile'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
               'Cookie': 'your cookies'
    }
    try:
        response = requests.get(url,headers = headers ,timeout = 10)
    except Exception as e :
        print(e)
        return True
     
    r =  response.text
    soup = BeautifulSoup(r, 'lxml')
    online_time = soup.select('ul[id="pbbs"] li')[0].text
    print(online_time)

    return False
 
if __name__ == '__main__':
    while True:
        t = ruisi()
        if t:
            continue
        time.sleep(600)