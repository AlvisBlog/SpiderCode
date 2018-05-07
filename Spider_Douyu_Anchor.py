#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-22 21:08'
_readme_="获取斗鱼直播信息"

import requests
import re
import xlwt
import json
import openpyxl
import time

#数据处理
class CategoryData:

    #初始化分类存储列表
    def __init__(self):
        self.Total_BigCategoryInfo=[]
        self.Total_CategoryInfo=[]
        self.Total_CategoryUrl = []
        self.Total_CategoryName=[]
        self.Total_LOL_AnchorInfo=[]

    #获取总分类
    def Get_Total_BigCategory_Data(self):
        # 总分类url地址
        url = "https://www.douyu.com/directory"
        try:
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
                self.Total_BigCategoryInfo.append((big_Category_name, big_Category_url))
            with open("douyu.log","a+") as f:
                f.write("已获取总分类数据,一共有%s个总分类 "%len(self.Total_BigCategoryInfo)+time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        except Exception as re_error:
            with open("douyu.log","a+") as f:
                f.write("页面无法相应,错误:%s  "%re_error+time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        return self.Total_BigCategoryInfo

    #保存总分类
    def Save_Total_BigCategory_Data(self):
        with open("douyu.log", 'a+') as f:
            f.write("检查获取总分类函数返回的总分类数据为%s  "%len(self.Total_BigCategoryInfo) + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.close()
        try:
            # 存在文件则进行加载
            wb = openpyxl.load_workbook(filename="斗鱼.xlsx")
        except Exception as e:
            with open("douyu.log", 'a+') as f:
                f.write("斗鱼.xlsx文件名不存在,进行创建  " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.close()
            # 不存在则进行创建
            wb = openpyxl.Workbook()
        # 获取所有的表
        all = wb.sheetnames
        # 删除表Sheet
        name = 'Sheet'
        if name in all:
            del wb['Sheet']
        # 创建新表
        ws = wb.create_sheet()
        # 为新表命名
        ws.title ='斗鱼总分类'
        ws.cell(row=1, column=1, value='总分类名称')
        ws.cell(row=1, column=2, value='总分类Url')
        for i in range(len(self.Total_BigCategoryInfo)):
            try:
                ws.cell(row=i+2, column=1, value=self.Total_BigCategoryInfo[i][0])
                ws.cell(row=i+2, column=2, value=self.Total_BigCategoryInfo[i][1])
            except Exception as BigCategoryInfo_error:
                with open("douyu.log", 'a+') as f:
                    f.write("无法写入数据,错误:%s  "%BigCategoryInfo_error + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    f.close()
        wb.save("斗鱼.xls")

    #获取各个总分类之下的小分类
    def Get_Total_Category_Data(self):
        for i in range(1,len(self.Total_BigCategoryInfo)):
            #获取大分类的名称及url地址
            url_big_category=self.Total_BigCategoryInfo[i][1]
            name_big_category=self.Total_BigCategoryInfo[i][0]
            #print("大分类:"+name_part_bigcategory+",url:"+url_part_bigcategory)
            #获取各个大分类的页面源代码
            html=requests.get(url_big_category).text
            #获取各个大分类的子分类所在数据区
            contents=re.findall('<ul id="live-list-contentbox">(.*?)</ul>',html,re.S)[0]
            #获取所有的子分类名称
            name_sub_category=re.findall('<p class="title">(.*?)</p>',contents,re.S)
            #获取所有的子分类url
            url=re.findall('href="(.*?)"',contents,re.S)
            #为url添加https://www.douyu.com
            url_sub_category = []
            for i in range(len(url)):
                url_sub_category.append("https://www.douyu.com" + url[i])
            self.Total_CategoryInfo.append(((name_big_category,name_sub_category),(url_big_category,url_sub_category)))
            self.Total_CategoryUrl.append(url_sub_category)
            self.Total_CategoryName.append(name_sub_category)

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

    def Get_Anchor_Data(self):
        self.Get_Total_Category_Data()
        anchorinfo=[]
        impress=[]
        all_tag_impress=[]
        for category_urls in self.Total_CategoryUrl:
            for category_url in category_urls:
                response=requests.get(category_url)
                html=response.text
                anchorname = re.findall('<span class="dy-name ellipsis fl">(.*?)</span>', html, re.S)
                anchorlink = re.findall('data-sub_rt="0" href="(.*?)"', html, re.S)
                anchortitle=re.findall('<h3 class="ellipsis">(.*?)</h3>',html,re.S)
                anchorhot=re.findall('<span class="dy-num fr"  >(.*?)</span>',html,re.S)
                anchortag=re.findall('<span class="tag ellipsis">(.*?)</span>',html,re.S)
                content = re.findall('<div class="impress-tag-list">(.*?)</div>', html, re.S)
                for line in content:
                    impress.append((line.strip()))
                for i in range(len(impress)):
                    tag_impress = re.findall('tags/(.*?)</span>', impress[i], re.S)
                    all_tag_impress.append(tag_impress)
                for i in range(len(anchorhot)):
                    try:
                        anchorinfo.append((anchorname[i],"https://www.douyu.com" + anchorlink[i],anchortitle[i].strip(),anchorhot[i].strip(),anchortag[i],all_tag_impress[i]))
                    except Exception as e:
                        print(e)
        f = xlwt.Workbook()
        sheet01 = f.add_sheet("主播信息")
        sheet01.write(0, 0, "主播名称")
        sheet01.write(0, 1, "主播房间")
        sheet01.write(0, 2, "主播标题")
        sheet01.write(0, 3, "主播热度")
        sheet01.write(0, 4, "主播类别")
        sheet01.write(0, 5, "主播印象")
        i = 1
        for anchor in anchorinfo:
            sheet01.write(i, 0, anchor[0])
            sheet01.write(i, 1, anchor[1])
            sheet01.write(i, 2, anchor[2])
            sheet01.write(i, 3, anchor[3])
            sheet01.write(i, 4, anchor[4])
            sheet01.write(i, 5, anchor[5])
            i = i + 1
        f.save("斗鱼直播主播信息.xls")



#主函数运行
if __name__=="__main__":
    #实例化
    Spider = CategoryData()
    Spider.Get_Total_BigCategory_Data()
    Spider.Get_Total_Category_Data()
    print(Spider.Total_CategoryInfo[0])
    print(Spider.Total_CategoryName)
    print(Spider.Total_CategoryUrl)