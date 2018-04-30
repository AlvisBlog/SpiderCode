#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-29 23:37'

import re
import requests
from selenium import webdriver
import xlwt
from time import sleep
url='http://www.80txt.com/txtml_46785.html'
response=requests.get(url)
html=response.text.encode('ISO-8859-1').decode('utf8')
content=re.findall('<li><a rel="nofollow" href=(.*?)/a></li>',html,re.S)
chapter_info=[]
chapter_url=[]
chapter_name=[]
chapter_content=[]
for i in range(len(content)):
    chapter_url.append(re.findall('"(.*?)"',content[i],re.S)[0])
for i in range(len(content)):
    chapter_name.append(re.findall('>(.*?)<',content[i],re.S)[0])
# for link in chapter_url:
#     sleep(5)
#     response2=requests.get(link)
#     sleep(5)
#     html2=response2.text
#     chapter_content.append(re.findall('<div class="book_content" id="content">(.*?)<div',html2,re.S)[0])
for i in range(len(content)):
    chapter_info.append((re.findall('"(.*?)"',content[i],re.S)[0],re.findall('>(.*?)<',content[i],re.S)[0]))
f=xlwt.Workbook()
sheet=f.add_sheet("小说章节信息")
sheet.write(0,0,"章节名")
sheet.write(0,1,"章节链接")
for j in range(len(chapter_info)):
    sheet.write(1 + j, 0, chapter_info[j][1])
    sheet.write(1 + j, 1, chapter_info[j][0])
f.save("我欲封天.xls")
print(chapter_url)
print(chapter_name)
print(chapter_content)