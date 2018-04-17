# -*- coding: UTF-8 -*-
_Author_ = 'Alvis'
_Date_ = '21:51 2018-03-26'
_README_='淘宝信息爬取'

import re
import requests
import json
import time
import xlwt


DATA=[]

#url地址
url="https://s.taobao.com/search?q=python&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180326&ie=utf8"

#发送Http请求,并接收返回
response=requests.get(url)

#html源码
html=response.text
#print(html)

#分析找出信息，“.*?”代表非贪婪匹配；
# “.”匹配任意可见字符，如换行符，空格符无法进行匹配,需要加上re.S，如果没有加上，则输出结果print(content)为空列表：[]
#[0]由于输出的content结果中，我们需要的信息应该为其中的字典，需要加上[0]，将信息取出,信息取出之后为一个字符串
#strip去掉content前后端的空格,
#[:-1]去掉尾部的分号
#请注意我：妈蛋“g_page_config = (.*?)”，这个“=”两边各有一个空格也不知道为什么要加，靠
content=re.findall(u'g_page_config = (.*?)g_srp_loadCss',html,re.S)[0].strip()[:-1]
#调试输出content内容，该其输出内容复制后，在www.json.con粘贴，进行结构分析
#print(content)
#调试输出content类型
#print(type(content))

#格式化json
content=json.loads(content)
#根据www.json.cn的结构分析进行结构数据取出
#获取商品信息列表，商品名称，标题，标价，购买人数，是否包邮，是否天猫，地区，店名，url
data_list=content['mods']['itemlist']['data']['auctions']
#调试输出data_list内容
#print(data_list)
#调试输出content类型，为字典
#print(type(content))
#调试输出content内容
#print(content)

#提取数据，分析content结构
for item in data_list:
    #调试输出item，每一条item都为独立的信息，
    #print(item)
    temp={
        'title':item['title'],
        'view_price': item['view_price'],
        'view_sales': item['view_sales'],
        'view_fee': '否' if float(item['view_fee']) else '是',
        'isTmall': '是' if item['shopcard']['isTmall'] else '否',
        'area': item['item_loc'],
        'name': item['nick'],
        'detail_url': item['detail_url'],
    }
#每次获取完数据就加入DATA列表里面
    DATA.append(temp)
#调试输出temp内容
#print(temp)
#调试查看获取的数据条数，一开始只有36条,真正的条数会有48条，而首页存在12条异步加载的数据,则来自于一条api的请求
#print(len(DATA))

#需要cookie保持,验证，将第一次response的cookies传给第二次
cookies=response.cookies

url2="https://s.taobao.com/api?_ksTS=1522072777204_224&callback=jsonp225&ajax=true&m=customized&stats_click=search_radio_all:1&q=python&s=36&imgfile=&initiative_id=staobaoz_20180326&bcoffset=0&js=1&ie=utf8&rn=8c0acb1785ec2c68d3a3e9a3d532d29a"

response2=requests.get(url2,cookies=cookies)

html2=response2.text

#调试输出html2
#print(html2)

#“.*”贪婪匹配
content=re.findall(r'{.*}',html2)[0]

#调试输出content
#print(content)

#格式化json
content=json.loads(content)

#调试输出content
#print(content)

data_list=content['API.CustomizedApi']['itemlist']['auctions']

#提取数据，分析content结构
for item in data_list:
    #调试输出item，每一条item都为独立的信息，
    #print(item)
    temp={
        'title':item['title'],
        'view_price': item['view_price'],
        'view_sales': item['view_sales'],
        'view_fee': '否' if float(item['view_fee']) else '是',
        'isTmall': '是' if item['shopcard']['isTmall'] else '否',
        'area': item['item_loc'],
        'name': item['nick'],
        'detail_url': item['detail_url'],
    }
#每次获取完数据就加入DATA列表里面
    DATA.append(temp)
#调试输出最终的数据条数，为48条
#print(len(DATA))



#翻页获取数据

#将cookies保持下来
cookies=response2.cookies

for i in range(1,2):
    ktsts=time.time()
    _ksTS='%s_%s' % (int(ktsts*1000),str(ktsts)[-3:])
    callback="jsonp%s" % (int(str(ktsts)[-3:]) + 1)
    data_value=44 * i
    #翻页逻辑
    url="https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&_ksTS={}&callback={}&q=python&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180327&ie=utf8&bcoffset=4&ntoffset=0&p4ppushleft=1%2C48".format(data_value,_ksTS,callback)
    #cookies保持
    response3=requests.get(url,cookies=cookies)
    #调试输出
    #print(response3.text)
    html=response3.text
    data_list = content['API.CustomizedApi']['itemlist']['auctions']
    # 提取数据
    for item in data_list:
        # 调试输出item，每一条item都为独立的信息，
        # print(item)
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        # 每次获取完数据就加入DATA列表里面，根据翻页数最终得到DATA的数目
        DATA.append(temp)
#调试输出最终的数据条数
#print(len(DATA))

#画图

#1.包邮和不包邮的比例
# data1={'包邮': 0, '不包邮': 0}
#
# #2.淘宝和天猫的比例
# data2={'天猫': 0, '淘宝': 0}
#
# #3.地区的分布
# data3={}
#
# for item in DATA:
#     if item['view_fee']=='否':
#         data1['不包邮'] +=1
#     else:
#         data1['包邮'] += 1
#     if item['isTmall']=='是':
#         data2['天猫'] +=1
#     else:
#         data2['淘宝'] += 1
#     data3[item['area'].split(' ')[0]] = data3.get(item['area'].split(' ')[0], 0) + 1
# print(data1)
# draw.pie(data1, '是否包邮')
# draw.pie(data2, '是否天猫')
# draw.pie(data3, '地区分布')

#持久化

f=xlwt.Workbook(encoding='utf8')
sheet01 = f.add_sheet(u'sheet1')
#写标题
sheet01.write(0, 0, '标题')
sheet01.write(0, 1, '标价')
sheet01.write(0, 2, '购买人数')
sheet01.write(0, 3, '是否包邮')
sheet01.write(0, 4, '是否天猫')
sheet01.write(0, 5, '地区')
sheet01.write(0, 6, '店名')
sheet01.write(0, 7, 'url')
#写内容
for i in range(len(DATA)):
    sheet01.write(i+1, 0, DATA[i]['title'])
    sheet01.write(i+1, 1, DATA[i]['view_price'])
    sheet01.write(i+1, 2, DATA[i]['view_sales'])
    sheet01.write(i+1, 3, DATA[i]['view_fee'])
    sheet01.write(i+1, 4, DATA[i]['isTmall'])
    sheet01.write(i+1, 5, DATA[i]['area'])
    sheet01.write(i+1, 6, DATA[i]['name'])
    sheet01.write(i+1, 7, DATA[i]['detail_url'])
f.save(u'搜索结果.xls')