#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-05-02 12:09'

# SSL证书验证
import requests
import re
import xlwt
from requests.packages import urllib3
f=xlwt.Workbook()
sheet=f.add_sheet("我欲封天")
sheet.write(0,0,"章节名")
sheet.write(0,1,"章节链接")
sheet.write(0,2,"章节内容")
chapter_url=[]
chapter_info=[]
chapter_content=[]
response=requests.get("https://www.xxbiquge.com/1_1339/",verify=False)
urllib3.disable_warnings()
html=response.text.encode('ISO-8859-1').decode('utf8')
content=re.findall('<dl>(.*?)</dl>',html,re.S)
#章节部分链接
chapter_url_content=re.findall('<dd><a href="(.*?)">',content[0],re.S)
#章节名
chapter_name=re.findall('">(.*?)</a>',content[0],re.S)
#章节补全链接
for link in chapter_url_content:
    chapter_url.append("https://www.xxbiquge.com"+link)
print(len(chapter_url))
print(len(chapter_name))
#章节内容
num=1
for i in range(len(chapter_url)):
    try:
        response1 = requests.get(chapter_url[i])
        html1 = response1.text.encode('ISO-8859-1').decode('utf8')
        print(num)
        print(re.findall('<div id="content">(.*?)</div>', html1, re.S)[0].strip())
        sheet.write(1 + i, 0, chapter_name[i])
        sheet.write(1 + i, 1, chapter_url[i])
        sheet.write(1 + i, 2, re.findall('<div id="content">(.*?)</div>', html1, re.S)[0].strip())
        num=num+1
        #chapter_content.append(re.findall('<div id="content">(.*?)</div>', html1, re.S)[0].strip())
    except Exception as e:
        print(e)
        break
print(len(chapter_content))

f.save("我欲封天.xls")