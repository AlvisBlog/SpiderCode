#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-05-02 19:21'

import requests
import re
import openpyxl

#获取章节名称及链接，
def GetChapterData(url):
    global chapter_name,chapter_url
    chapter_url=[]
    #返回信息
    response=requests.get(url)
    #源网页代码
    html=response.text.encode('ISO-8859-1').decode('utf8')
    #网页中包含章节名称及链接的数据
    content = re.findall('<dl>(.*?)</dl>', html, re.S)
    # 获取章节部分链接，缺少"https://www.xxbiquge.com"
    chapter_url_content = re.findall('<dd><a href="(.*?)">', content[0], re.S)
    # 获取章节名称
    chapter_name = re.findall('">(.*?)</a>', content[0], re.S)
    # 获取章节链接，补全"https://www.xxbiquge.com"
    for link in chapter_url_content:
        chapter_url.append("https://www.xxbiquge.com" + link)
    return chapter_url,chapter_name

#获取章节内容
def ChapterContent():
    global chapter_content
    chapter_content=[]
    for i in range(len(chapter_url)):
        response1 = requests.get(chapter_url[i])
        html1 = response1.text.encode('ISO-8859-1').decode('utf8')
        chapter_content.append(re.findall('<div id="content">(.*?)</div>', html1, re.S)[0])
    return chapter_content

#将章节名称及链接、内容放置到列表
def ChapterInfo():
    global chapter_info
    chapter_info=[]
    for i in range(len(chapter_url)):
        chapter_info.append((chapter_name[i], chapter_url[i], re.findall('<div id="content">(.*?)</div>', html1, re.S)[0]))

#保存数据
def SaveInfo():
    # 写入文件
    wb = openpyxl.Workbook()
    ws1 = wb.get_sheet_by_name('Sheet')
    ws1.title = "我欲封天"
    ws1['A1'] = "章节名称"
    ws1['B1'] = "章节地址"
    ws1['C1'] = "章节内容"
    for row in chapter_info:
        ws1.append(row)
    wb.save("小说.xlsx")