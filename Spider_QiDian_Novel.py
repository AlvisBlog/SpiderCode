#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-29 20:56'

import re
import requests
import xlwt
book_name=[]
book_author=[]
book_type=[]
book_intro=[]
book_status=[]
book_word=[]
mapping_word={"&#100183;":".","&#100185;":"0","&#100190;":"1","&#100191;":"2","&#100181;":"3",
              "&#100188;":"4","&#100186;":"5","&#100192;":"6","&#100189;":"7","&#100184;":"8",
              "&#100187;":"9"}
num=1
f=xlwt.Workbook()
sheet=f.add_sheet("小说信息")
sheet.write(0,0,"小说名称")
sheet.write(0,1,"小说作者")
sheet.write(0,2,"小说类型")
sheet.write(0,3,"小说简介")
sheet.write(0,4,"小说状态")
sheet.write(0,5,"小说字数")

for page in range(1,44713):
    try:
        print("正在获取第%s页所有小说信息" % page)
        url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%s'%page
        response=requests.get(url)
        html=response.text
        name_contents = re.findall('<h4><a href="//book.qidian.com/info/(.*?)</a></h4>', html, re.S)
        author_contents=re.findall('<a class="name" href="//my.qidian.com/author/(.*?)</a>',html,re.S)
        type_contents=re.findall('</em><a href="//www.(.*?)</a>',html,re.S)
        intro_contents=re.findall('<p class="intro">(.*?)</p>',html,re.S)
        status_contents=re.findall('</em><span >(.*?)</span>',html,re.S)
        word_contents=re.findall('</style><span class="gVRTUBas">(.*?)</span>',html,re.S)
        for i in range(len(name_contents)):
            book_name.append(name_contents[i].split(">")[1])
            book_author.append(author_contents[i].split(">")[1])
            book_type.append(type_contents[i].split(">")[1])
            book_intro.append(intro_contents[i].strip())
            book_status.append(status_contents[i])
            print("已获取%s本小说信息" % num)
            sheet.write(num, 0, name_contents[i].split(">")[1])
            sheet.write(num, 1, author_contents[i].split(">")[1])
            sheet.write(num, 2, type_contents[i].split(">")[1])
            sheet.write(num, 3, intro_contents[i].strip())
            sheet.write(num, 4, status_contents[i])
            num=num+1
    except Exception as reason:
        print(reason)
        break
f.save("起点中文网小说信息2.xls")
print(len(book_name))
