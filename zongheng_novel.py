#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-30 1:44'


import requests
import re
import xlwt
Novel_Info=[]
Link=[]
content=[]
def Get_chapter_detail():
    url='http://book.zongheng.com/showchapter/685640.html'
    response=requests.get(url)
    html=response.text
    global Name,WordNum,UpDate
    Name=re.findall('chapterName="(.*?)"',html,re.S)
    WordNum=re.findall('wordNum="(.*?)"',html,re.S)
    UpDate=re.findall('title="最后更新时间:(.*?)字',html,re.S)
    for i in range(len(re.findall('<td(.*?)</td>',html,re.S))):
        Link.append(re.findall('href="(.*?)"',re.findall('<td(.*?)</td>',html,re.S)[i],re.S))

def Get_chapter_content():
    for chapter_url in Link:
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        html2 = requests.get(url=chapter_url, headers=header).text
        content.append(re.findall('<div id="readerFs" class="">(.*?)</div>', html2, re.S)[0].split("</script>")[1].strip())

def Collect_chapter_info():
    for i in range(len(Name)):
        Novel_Info.append((Name[i],Link[i][0],UpDate[i],WordNum[i]))

def Save_chapter_info():
    f=xlwt.Workbook()
    sheet=f.add_sheet("元尊")
    sheet.write(0,0,"章节名称")
    sheet.write(0,1,"章节链接")
    sheet.write(0,2,"章节更新时间")
    sheet.write(0,3,"章节字数")
    for i in range(len(Novel_Info)):
        sheet.write(1 + i, 0, Novel_Info[i][0])
        sheet.write(1 + i, 1, Novel_Info[i][1])
        sheet.write(1 + i, 2, Novel_Info[i][2])
        sheet.write(1 + i, 3, Novel_Info[i][3])
    f.save("小说章节.xls")

Get_chapter_detail()
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
response1=requests.get(url=Link[0][0], headers=header)
html1 = response1.text
content.append(re.findall('<div id="readerFs" class="">(.*?)</div>', html1, re.S)[0].split("</script>")[1].strip())
cookies=response1.cookies
for i in range(1,len(Link)-1):
    response2=requests.get(url=Link[i][0],cookies=cookies,headers=header)
    html2 = response2.text
    content.append(re.findall('<div id="readerFs" class="">(.*?)</div>', html2, re.S)[0].split("</script>")[1].strip())
