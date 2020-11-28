import re

reg = r'\d+'
print(re.search(reg, 'abc123cd'))

r'''
    特殊字符：\r回车 \n换行 \t制表 \\反斜杠本身
    \d      0-9之间的一个数值
    \b      单词结尾，包括各种空白字符或字符串结尾
    \s      任何空白字符  等价于[\r\n\x20\t\f\v]
    \w      包括下划线的单词字符  等价于[a-zA-Z0-9_]
         
    +       重复前面一个匹配字符  一次或者多次  (必须有)
    *       重复前面一个匹配字符  零次或者多次  (可有可无)
    ?       重复前面一个匹配字符  零次或者一次  (最多一次)
    {n}     匹配n次
    {n,}    匹配至少n次
    {n,m}   匹配至少n次且最多m次
    .       代表任何一个字符，（没有特别声明时不代表字符'\\n'）
    |       或           eg. r'ab|ba' 匹配ab或ba都可以
    []      []中的字符任意选一个，如果字符是ASCII码中连续的一组，可以使用'-'连接
    ^       出现在[]第一个字符位置时，表示取反      eg. [^ab0-9] 表示不是a、b、0-9的字符
    
    ^       匹配字符串的开头位置      eg.  re.search(r'^ab', 'cabcab')  # None
    $       匹配字符串的结尾位置      eg.  re.search(r'ab$', 'abcab')   # span=(3, 5), match='ab'
    ()      划分一个整体，常与 + * ? 等连续使用
'''
# 匹配找出英文句子中的所有单词
s = 'I am testing search function'
# reg = r'[A-Za-z]+'    # 这俩效果一样
reg = r'[A-Za-z]+\b'
m = re.search(reg, s)
while m is not None:
    start = m.start()
    end = m.end()
    print(s[start:end])
    s = s[end:]
    m = re.search(reg, s)


