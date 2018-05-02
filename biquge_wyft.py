#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-05-02 12:09'

# SSL证书验证
import requests
import re
import openpyxl
from requests.packages import urllib3
chapter_url=[]
chapter_info=[]
chapter_content=[]

response=requests.get("https://www.xxbiquge.com/1_1339/",verify=False)
urllib3.disable_warnings()
html=response.text.encode('ISO-8859-1').decode('utf8')
content=re.findall('<dl>(.*?)</dl>',html,re.S)
#获取章节部分链接
chapter_url_content=re.findall('<dd><a href="(.*?)">',content[0],re.S)
#获取章节名
chapter_name=re.findall('">(.*?)</a>',content[0],re.S)
#补全章节链接
for link in chapter_url_content:
    chapter_url.append("https://www.xxbiquge.com"+link)
#获取章节内容
num=1
print(len(chapter_url))
print(len(chapter_name))
for i in range(len(chapter_url)-1):
    response1=requests.get(chapter_url[i])
    html1=response1.text.encode('ISO-8859-1').decode('utf8')
    chapter_content.append(re.findall('<div id="content">(.*?)</div>',html1,re.S)[0])
    print(num)
    print(re.findall('<div id="content">(.*?)</div>',html1,re.S)[0])
    print(num)
    num=num+1
    chapter_info.append((chapter_name[i],chapter_url[i],re.findall('<div id="content">(.*?)</div>',html1,re.S)[0]))
#写入文件
wb = openpyxl.Workbook()
ws1 = wb.get_sheet_by_name('Sheet')
ws1.title = "我欲封天"
ws1['A1'] = "章节名称"
ws1['B1'] = "章节地址"
ws1['C1'] = "章节内容"
for row in chapter_info:
    ws1.append(row)
wb.save("小说.xlsx")