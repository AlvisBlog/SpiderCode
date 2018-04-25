#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-22 21:08'
_readme_="获取斗鱼直播信息"

import requests
import re
import xlwt
import json

#数据处理
class CategoryData:

    #初始化分类存储列表
    def __init__(self):
        self.Total_BigCategoryInfo=[]
        self.Total_CategoryInfo=[]
        self.Total_CategoryUrl = []
        self.Total_CategoryName=[]
        self.Total_LOL_AnchorInfo=[]

    #获取大分类
    def Get_Total_BigCategory_Data(self):
        # 总分类url地址
        url = "https://www.douyu.com/directory"
        # 获取页面信息内容
        response = requests.get(url)
        html = response.text
        # 获取关键信息，包含所有的大分类囊括信息
        content1 = re.findall('<div class="classify-li">(.*?)</div>', html, re.S)[0]
        content2 = re.findall('<a(.*?)</li>', content1, re.S)
        # 截取关键信息
        for i in content2:
            big_Category_name = re.findall('>(.*?)</a>', i, re.S)[0].strip()
            big_Category_url = "https://www.douyu.com" + re.findall('data-href="(.*?)"', i, re.S)[0]
            self.Total_BigCategoryInfo.append((big_Category_name,big_Category_url))

    #保存大分类
    def Save_Total_BigCategory_Data(self):
        # 创建Excel
        f = xlwt.Workbook()
        # 创建大分类信息存储的excel表
        sheet01 = f.add_sheet("斗鱼直播总分类信息")
        sheet01.write(0, 0, "分类名")
        sheet01.write(0, 1, "分类url地址")
        for i in range(len(self.Total_BigCategoryInfo)):
            sheet01.write(i + 1, 0, self.Total_BigCategoryInfo[i][0])
            sheet01.write(i + 1, 1, self.Total_BigCategoryInfo[i][1])
        f.save("斗鱼直播总分类信息.xls")

    #获取所有分类
    def Get_Total_Category_Data(self):
        self.Get_Total_BigCategory_Data()
        for i in range(1,len(self.Total_BigCategoryInfo)):
            #获取大分类的名称及url地址
            url_bigcategory=self.Total_BigCategoryInfo[i][1]
            name_bigcategory=self.Total_BigCategoryInfo[i][0]
            #print("大分类:"+name_part_bigcategory+",url:"+url_part_bigcategory)
            #获取各个大分类的页面源代码
            html=requests.get(url_bigcategory).text
            #获取各个大分类的子分类所在数据区
            contents=re.findall('<ul id="live-list-contentbox">(.*?)</ul>',html,re.S)[0]
            #获取所有的子分类名称
            name_subcategorys=re.findall('<p class="title">(.*?)</p>',contents,re.S)
            #获取所有的子分类url
            url=re.findall('href="(.*?)"',contents,re.S)
            #为url添加https://www.douyu.com
            url_subcategorys = []
            for i in range(len(url)):
                url_subcategorys.append("https://www.douyu.com" + url[i])
            self.Total_CategoryInfo.append(((name_bigcategory,name_subcategorys),(url_bigcategory,url_subcategorys)))
            self.Total_CategoryUrl.append(url_subcategorys)
            self.Total_CategoryName.append(name_subcategorys)

    #保存所有分类
    def Save_Total_Category_Data(self):
        # 存储分类信息
        f = xlwt.Workbook()
        # 根据分类名称创建工作表
        for i in range(len(self.Total_CategoryInfo)):
            # 创建大分类工作表
            sheet01 = f.add_sheet(self.Total_CategoryInfo[i][0][0])
            sheet01.write(0, 0, "总分类名")
            sheet01.write(1, 0, self.Total_CategoryInfo[i][0][0])
            sheet01.write(0, 1, "总分类url")
            sheet01.write(1, 1, self.Total_CategoryInfo[i][1][0])
            sheet01.write(0, 2, "子分类名")
            sheet01.write(0, 3, "子分类url地址")
            for j in range(len(self.Total_CategoryInfo[i][0][1])):
                # 写入子分类名称
                sheet01.write(j + 1, 2, self.Total_CategoryInfo[i][0][1][j])
                # 写入子分类url
                sheet01.write(j + 1, 3, self.Total_CategoryInfo[i][1][1][j])
        f.save("斗鱼直播所有分类信息.xls")

    #获取分类下的主播：主播名，房间链接，标题，热度
    def Get_LOL_AnchorInfo(self):
        for page in range(1,7):
            #LOL主播翻页API
            url2='https://www.douyu.com/gapi/rkc/directory/2_1/%s'%page
            response2=requests.get(url2)
            html2=response2.text
            content=json.loads(html2)
            for data in content['data']['rl']:
                self.Total_LOL_AnchorInfo.append([data['nn'],"https://www.douyu.com" + data['url'],data['rn'],data['ol']])

    #保存主播信息
    def Save_LOL_AnchorInfo(self):
        f = xlwt.Workbook()
        sheet01 = f.add_sheet("LOL主播信息")
        sheet01.write(0, 0, "主播名称")
        sheet01.write(0, 1, "主播房间")
        sheet01.write(0, 2, "主播标题")
        sheet01.write(0, 3, "主播热度")
        i = 1
        for LOL_AnchorInfo in self.Total_LOL_AnchorInfo:
            sheet01.write(i, 0, LOL_AnchorInfo[0])
            sheet01.write(i, 1, LOL_AnchorInfo[1])
            sheet01.write(i, 2, LOL_AnchorInfo[2])
            sheet01.write(i, 3, LOL_AnchorInfo[3])
            i = i + 1
        f.save("斗鱼直播_LOL主播信息.xls")



#主函数运行
if __name__=="__main__":
    #实例化
    a = CategoryData()
    a.Get_LOL_AnchorInfo()
    a.Save_LOL_AnchorInfo()