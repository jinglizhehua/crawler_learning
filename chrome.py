from selenium import webdriver
import json

# 启动浏览器
# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com')

# chrome_options = webdriver.ChromeOptions()
# # 使用headless无界面浏览器模式
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# # 启动浏览器，获取网页源代码
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.get('https://www.baidu.com')
# print('browser text = {}'.format(browser.page_source))
# browser.quit()

def getCookies(url, file_name):
    browser = webdriver.Chrome()
    browser.get(url)
    input('登录后请按回车键...')
    cookies = browser.get_cookies()
    jsonCookies = json.dumps(cookies)
    browser.close()

    with open(file_name + '.txt', 'w') as file:
        file.write(jsonCookies)
        file.close()

# u = 'https://www.52pojie.cn/member.php?mod=logging&action=login'
# getCookies(u, 'cookie_52pojie')

u = 'https://space.bilibili.com/4377337/fans/fans'
getCookies(u, 'cookie_bilibili')
