from bs4 import BeautifulSoup
r"""
HTML文档结构：
                <head>  --  <title>
            /
    <html>
            \
                <body>  --  <p>、<a>、……

    <> 为一个tag元素或element元素，tag元素的名称不区分大小写。
    一个tag元素可以有很多属性。     eg.  <p class="title">
    除了tag元素外，穿插于tag元素之间的那些文本也是元素，称为text元素。  eg.  <title>The Dormouse's story</title>

HTML文档树：
    eg.
    <html>
    <head><title>Demo</title></head>
    <body>
    <div>A<p>B</p>C</div>
    <span>D</span>
    </body>
    </html>
    其对应的文档树：
                 <html>
               /       \
           <head>     <body>
          /          /     \
     <title>      <div>   <span>
      /         /   |   \      \
   Demo        A   <p>   B      D
"""

''' BeautifulSoup装载HTML文档 '''
# soup = BeautifulSoup(doc, 'lxml') # 用'lxml'解析器解析doc
# soup.prettify()  # 把soup对象
doc = '''
<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p ckass="story">
Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>, 
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and 
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
</p>
<p class="story">...</p>
</body>
</html>
'''
soup = BeautifulSoup(doc, 'lxml')
# print(soup.prettify())      # prettify() 格式化    它会自动补全缺失的元素，修正大小写

''' BeautifulSoup查找文档元素 '''
# 查找HTML元素
# find_all(), find()
tag = soup.find('title')
print(type(tag), tag)
tags = soup.find_all('a')
for tag in tags:
    print(tag)
# 查找第一个<a>元素
tag = soup.find('a')
print(tag)
# 查找class='title'的<p>元素
tag = soup.find('p', attrs={'class': 'title'})
print(tag)
# 查找class='sister'的元素
tags = soup.find_all(name=None, attrs={'class': 'sister'})
for tag in tags:
    print(tag)

# 获取元素的属性值
# 查找文档中的所有超链接地址
tags = soup.find_all('a')
for tag in tags:
    print(tag['href'])

# 获取元素包含的文本值
# 查找文档中所有<a>包含的文本值
tags = soup.find_all('a')
for tag in tags:
    print(tag.text)
# 查找文档中所有<p>包含的文本值
tags = soup.find_all('p')
for tag in tags:
    print(tag.text)     # <p>结点下的所有文本结点的组合值

# 高级查找（一般find和find_all都能满足基本的需要，如果还不能，那么可以设计一个查找函数来进行查找
# 查找文档中 href="http://example.com/lacie"的结点元素<a>
def myFilter(_tag):
    print(_tag.name)
    return _tag.name == 'a' and _tag.has_attr('href') and _tag['href'] == 'http://example.com/lacie'
tag = soup.find_all(myFilter)
print(tag)


''' BeautifulSoup遍历文档元素 '''
# 获取元素结点的父结点
tag = soup.find('a')
print('子:', tag)
tag = tag.parent
print('父:', tag)

# 获取元素结点的直接子元素结点
tag = soup.find('p')
print('子元素')
for x in tag.children:
    print(x)

# 获取元素结点的所有子孙元素结点
print('所有子孙')
for x in tag.descendants:
    print(x)

# 获取元素结点的所有兄弟结点
doc = '''
<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The<i>Dormouse's</i>story</b>Once upon a time ...</p>
</body>
</html>
'''
soup = BeautifulSoup(doc, 'lxml')
tag = soup.find('b')
print(tag.previous_sibling, '\n', tag.next_sibling)
tag = soup.find('i')
print(tag.previous_sibling, '\n', tag.next_sibling)

''' Beautiful使用CSS语法查找元素 '''
# [tagName][attName[=value]]  []表示可选； tagName是元素名称，不指定就是所有元素； attName是属性名称，value是他的值；
# tag.select(css) 返回一个tag的列表，只有一个元素也是一个列表
soup.select('a')                    # 查找所有<a>
soup.select('p a')                  # 查找所有<p>结点下的<a>
soup.select("p[class='story'] a")   # 查找所有属性class='story'的<p>结点下的所有<a>
soup.select('p[class] a')           # 查找所有具有属性class的<p>结点下的所有<a>
soup.select("a[id='link']")
soup.select('body head title')      # 查找<body>下面<head>下面的<title>
soup.select('body [class]')         # 查找<body>下面所有具有class属性的结点
soup.select('body [class] a')       # 查找<body>下面所有具有class属性的结点下面的<a>

# 属性的语法规则
"""
[attName]
[attName=value]
[attName^=value]    匹配属性值以指定值 开头 的每个元素
[attName$=value]    匹配属性值以指定值 结尾 的每个元素
[attName*=value]    匹配属性值中      包含 指定值的每个元素
"""

# select查找 子、子孙、兄弟 结点
"""
soup.select("div p")      # 查找所有<div>结点下的所有 子孙结点
soup.select("div > p")    # 查找所有<div>结点下的所有 直接子结点
soup.select("div ~ p")    # 查找所有<div>结点下的所有 兄弟结点
"""

