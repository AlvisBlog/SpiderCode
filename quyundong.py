#coding=utf8
import requests
import xlwt
import re
import json
def GetVenuesInfo():
    venues_info=[]
    for i in range(1,13):
        api='http://www.quyundong.com/index/businesslist?random=0.5960742008869808&page=%s'%i
        data=requests.get(api).text
        content=json.loads(data)
        for j in range(len(content['data']['data'])):
            venues_info.append((content['data']['data'][j]['name'],content['data']['data'][j]['address'],
                                content['data']['data'][j]['promote_price'],content['data']['data'][j]['comment_avg'],
                                content['data']['data'][j]['comment_count'],content['data']['data'][j]['price'],
                            content['data']['data'][j]['latitude'],content['data']['data'][j]['longitude']))
def GetCityInfo():
    city_info=[]
    url="http://www.quyundong.com"
    response=requests.get(url)
    html=response.text
    city_id=re.findall('data-cityId="(.*?)"',html,re.S)
    city_name=re.findall('data-cityName="(.*?)"',html,re.S)
    for i in range(len(city_id)):
        city_info.append((city_id[i],city_name[i]))
    return city_info
# f=xlwt.Workbook()
# sheet01 =f.add_sheet("场馆信息")
# sheet01.write(0,0,"场馆名")
# sheet01.write(0,1,"场馆地址")
# sheet01.write(0,2,"趣运动价格")
# sheet01.write(0,3,"球馆星级")
# sheet01.write(0,4,"评论数")
# sheet01.write(0,5,"其他价格")
# sheet01.write(0,6,"球馆纬度")
# sheet01.write(0,7,"球馆经度")
# for j in range(len(venues_info)):
#     sheet01.write(j + 1, 0, venues_info[j][0])
#     sheet01.write(j + 1, 1, venues_info[j][1])
#     sheet01.write(j + 1, 2, venues_info[j][2])
#     sheet01.write(j + 1, 3, venues_info[j][3])
#     sheet01.write(j + 1, 4, venues_info[j][4])
#     sheet01.write(j + 1, 5, venues_info[j][5])
#     sheet01.write(j + 1, 6, venues_info[j][6])
#     sheet01.write(j + 1, 7, venues_info[j][7])
# f.save("场馆信息.xls")
