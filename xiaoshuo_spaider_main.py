# @project 小说网站下载爬虫
# @author 任昱柯
# 功能 输入小说名字自动爬取所有章节 若不存在则提示不存在
# 先获取搜索小说的方法 --》搜索到小说给每个小说分配id让用户输入id来判断爬取哪一个小说
# 知道了爬取哪本——》获取小说目录列表（url）——》访问并解析存储
from lxml import html
import requests
import time
import random
import re
from bs4 import BeautifulSoup
import winshell   # 自动获取桌面路径
import os

print("/"*8+"小说*爬取"+"/"*8)
print("可以少输入但是不要输错")
name = input("输入小说/作者 名称：")
url = "https://www.biquge7.xyz/search?keyword={}".format(name)

# 请求头
headers ={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# 随机延时防检测
time.sleep(random.uniform(3,6))

# 发送请求获取数据
get_xsname = requests.get(url=url,headers=headers).text
getxsname = html.etree.HTML(get_xsname)  # 使用etree转换数据
# print(get_xsname) # 获取到的书籍名称页面
booknames = re.findall('alt="(.*?)" onerror',get_xsname) # 书名列表
booklistinfo = re.search('<div class="title">(.*?)</div>',get_xsname,re.S)
bookurls = re.findall('a href="(.*?)" title',booklistinfo.group(1)) # 书url列表


# 用来选取书籍
booknum =0
# 遍历下小说名字输出给用户
for i in booknames:
    booknum += 1
    print("{}:{}".format(booknum,i))
# 如果列表是空的
if booknum == 0:
    print("没有获取到书籍，请输入正确的书名或作者名")

# 挑选书籍
selectnum = int(input("请选择书的序号："))
bookurl1 = bookurls[(selectnum-1)]
bookurl ="https://www.biquge7.xyz"+bookurl1
# 获取小说章节列表
chapters_text=requests.get(url=bookurl,headers=headers).text
chapters_urls = re.search("<ul>(.*?)</ul>",chapters_text,re.S)
chapters_url = re.findall("<li>(.*?)</li>",chapters_urls.group(1))
chapters_nums=len(chapters_url)

# 写一下怎么保存到桌面的文件夹
win = winshell.desktop().split("/")[0] #桌面地址
root = win + "//" + booknames[(selectnum-1)]
if not os.path.exists(root):        # 是否存在文件夹 不存在则创建
        os.mkdir(root)

# 遍历章节进行爬取
for chapter in range(1,chapters_nums+1):
    chapterurl = "{}/{}".format(bookurl,chapter)
    book_chapter_text = requests.get(url=chapterurl,headers=headers).text
    book_chapter_text1 = BeautifulSoup(book_chapter_text)
    chaptersoup = BeautifulSoup(book_chapter_text,"lxml")
    chaptername = chaptersoup.title.string
    chaptertext = book_chapter_text1.select_one('body > div.box > div.list.list_text > div.text').get_text(separator='\n')

    # 输出章节内容
    print(chaptertext)
    print("文件{}保存成功".format(chaptername))
    # 保存为txt文件
    with open(root+"//"+chaptername+".txt", "w",encoding="utf-8") as file:
        file.write(chaptername+'\n'+chaptertext)