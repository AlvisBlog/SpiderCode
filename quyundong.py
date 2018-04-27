#coding=utf8
import requests
import xlwt
import re
import json
class Quyundong:

    def __init__(self):
        self.venues_info=[]
        self.city_info=[]

    def GetVenuesInfo(self):
        self.GetCityInfo()
        for j in range(len(self.city_info)):
            for i in range(1,13):
                api='http://www.quyundong.com/index/businesslist?random=0.5960742008869808&page=%s&city_id=%s'\
                    %(i,self.city_info[j][0])
                data=requests.get(api).text
                content=json.loads(data)
                for j in range(len(content['data']['data'])):
                    self.venues_info.append((content['data']['data'][j]['name'],content['data']['data'][j]['address'],
                                             content['data']['data'][j]['promote_price'],content['data']['data'][j]['comment_avg'],
                                        content['data']['data'][j]['comment_count'],content['data']['data'][j]['price'],
                                    content['data']['data'][j]['latitude'],content['data']['data'][j]['longitude']))

            # f = xlwt.Workbook()
            # sheet01 = f.add_sheet(self.city_info[j][1])
            # sheet01.write(0, 0, "场馆名")
            # sheet01.write(0, 1, "场馆地址")
            # sheet01.write(0, 2, "趣运动价格")
            # sheet01.write(0, 3, "球馆星级")
            # sheet01.write(0, 4, "评论数")
            # sheet01.write(0, 5, "其他价格")
            # sheet01.write(0, 6, "球馆纬度")
            # sheet01.write(0, 7, "球馆经度")
            # for j in range(len(self.venues_info)):
            #     sheet01.write(j + 1, 0, self.venues_info[j][0])
            #     sheet01.write(j + 1, 1, self.venues_info[j][1])
            #     sheet01.write(j + 1, 2, self.venues_info[j][2])
            #     sheet01.write(j + 1, 3, self.venues_info[j][3])
            #     sheet01.write(j + 1, 4, self.venues_info[j][4])
            #     sheet01.write(j + 1, 5, self.venues_info[j][5])
            #     sheet01.write(j + 1, 6, self.venues_info[j][6])
            #     sheet01.write(j + 1, 7, self.venues_info[j][7])


    def GetCityInfo(self):
        url="http://www.quyundong.com"
        response=requests.get(url)
        html=response.text
        city_id=re.findall('data-cityId="(.*?)"',html,re.S)
        city_name=re.findall('data-cityName="(.*?)"',html,re.S)
        for i in range(len(city_id)):
            self.city_info.append((city_id[i],city_name[i]))
        return self.city_info

if __name__=='__main__':
    a=Quyundong()
    a.GetVenuesInfo()
    print(a.venues_info )