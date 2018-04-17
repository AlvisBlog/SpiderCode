# -*- coding: UTF-8 -*-

_Author_ = 'Alvis'

_Date_ = '2018/4/14 14:40'

import requests
import re
import xlwt
import os
import time


#获取图片链接地址
def GetPictureLinks():
    #url地址
    url="http://588ku.com/tuku/keji.html"

    #发送Http请求,并接收返回
    response=requests.get(url)

    #获取网页源代码
    html=response.text

    Pic_urls=re.findall('original="(.*?)!/fh',html)

    return Pic_urls

#下载图片至目录image
def DownPicToIMG(links):
    try:
        os.mkdir('./image')
    except Exception as e:
        pass
    for i in range(len(links)):
        r=requests.get(links[i])
        with open('./image/%s_%s.jpg'%(i,time.time()),'wb') as f:
            f.write(r.content)

#下载链接保存到xls文件
def DownPiclinkToXLS(links):
    f=xlwt.Workbook(encoding='utf8')
    sheet01=f.add_sheet(u'sheet01')
    sheet01.write(0,0,'下载链接')
    for i in range(len(links)):
        sheet01.write(i+1,0,links[i])
    f.save(u'图片集.xls')



DownPicToIMG(GetPictureLinks())

DownPiclinkToXLS(GetPictureLinks())