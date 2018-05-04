#coding=utf8
_Author_ = 'Alvis'
_Date_ = '14:40 2018-05-04'

import requests
import re
from requests.packages import urllib3
import openpyxl

#球馆名称
venue_name=[]
#球馆地址
venue_address=[]
#球馆标签
venue_tag=[]
#球馆电话
venue_mobile=[]

def GetVenueInfo():
    for page in range(1,410):
        print("当前访问第%s页"%page)
        url='http://www.dongsport.com/venue/list-1004401-0-0-0-0-0-0-0-%s.html'%page
        try:
            response=requests.get(url)
            urllib3.disable_warnings()
        except Exception as error:
            with open("log.text","a+") as f:
                f.write("无法访问第%s页"%page+"错误为:%s"%error+"\n")
            continue
        html = response.text
        venue_content=re.findall('<div class="left v_l_text">(.*?)</div>',html,re.S)
        for content in venue_content:
            venue_name.append(re.findall('target="_blank">(.*?) ',content,re.S)[0].strip())
            venue_address.append(re.findall('<li>(.*?) ',content,re.S)[0].strip())
            venue_tag.append(re.findall('<li>(.*?)</li>',content,re.S)[2].strip())
            venue_mobile.append(re.findall('<b class="fontstyle4">(.*?) ',content,re.S)[0].strip())
        print("已获取第%s页数据"%page)

def SaveVenueInfo():
    try:
        wb=openpyxl.load_workbook(filename="场馆信息.xlsx")
    except Exception as e:
        wb=openpyxl.Workbook()
    # 获取所有的表
    all = wb.sheetnames
    # 删除表Sheet
    name = 'Sheet'
    if name in all:
        del wb['Sheet']
    ws=wb.create_sheet()
    ws.title='动网'
    ws.cell(row=1, column=1, value='场馆名称')
    ws.cell(row=1, column=2, value='场馆地址')
    ws.cell(row=1, column=3, value='场馆电话')
    ws.cell(row=1, column=4, value='场馆标签')
    for i in range(len(venue_mobile)):
        ws.cell(row=i + 2, column=1, value=venue_name[i])
        ws.cell(row=i + 2, column=2, value=venue_address[i])
        ws.cell(row=i + 2, column=3, value=venue_mobile[i])
        ws.cell(row=i + 2, column=4, value=venue_tag[i])
        print("已写入%s条数据"%(i+1))
    wb.save("场馆信息.xlsx")

def run():
    GetVenueInfo()
    SaveVenueInfo()

if __name__=="__main__":
    run()