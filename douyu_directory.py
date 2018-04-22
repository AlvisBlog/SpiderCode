#coding=utf8


_Author_ = 'Alvis'
_Date_ = '2018-04-22 21:08'
_readme_="获取斗鱼直播大分类信息"

import requests
import re
import xlwt

#大分类数据处理
class BigDiredtoryData:

    #初始化大分类存储空列表
    def __init__(self):
        self.BigDirectoryInfo=[]

    #获取大分类数据
    def Get_BigDirectory_Data(self):
        # 大分类url地址
        url = "https://www.douyu.com/directory"
        # 获取页面信息内容
        response = requests.get(url)
        html = response.text
        # 获取关键信息，包含所有的大分类囊括信息
        content1 = re.findall('<div class="classify-li">(.*?)</div>', html, re.S)[0]
        content2 = re.findall('<a(.*?)</li>', content1, re.S)
        # 截取关键信息
        for i in content2:
            big_directory_name = re.findall('>(.*?)</a>', i, re.S)[0].strip()
            big_directory_url = "https://www.douyu.com" + re.findall('data-href="(.*?)"', i, re.S)[0]
            self.BigDirectoryInfo.append((big_directory_name,big_directory_url))

    #存储大分类数据
    def Save_BigDirectory_Data(self):
        #存储分类信息
        f = xlwt.Workbook()
        # 创建大分类信息存储的excel表
        sheet01 = f.add_sheet("斗鱼大分类信息")
        sheet01.write(0, 0, "分类名")
        sheet01.write(0, 1, "分类url地址")
        for i in range(len(self.BigDirectoryInfo)):
            sheet01.write(i+1,0,self.BigDirectoryInfo[i][0])
            sheet01.write(i+1,1,self.BigDirectoryInfo[i][1])
        f.save("斗鱼直播分类信息.xls")

#主函数运行
if __name__=="__main__":
    #实例化
    a = BigDiredtoryData()
    a.Get_BigDirectory_Data()
    a.Save_BigDirectory_Data()