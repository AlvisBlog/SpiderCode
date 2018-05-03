#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-05-02 19:21'

import requests
import re
import openpyxl
from requests.packages import urllib3
from time import sleep

class Spider_bqg_novel:

    #初始化数据
    def __init__(self):
        #章节名列表
        self.chapter_name=[]
        #章节链接列表
        self.chapter_url=[]
        #章节内容
        self.chapter_content=[]
        #三者合并
        self.chapter_info=[]
        self.chapter_num=1

    #获取章节名称及链接、内容
    def GetChapterData(self,url):
        # 返回信息
        response = requests.get(url,verify=False)
        urllib3.disable_warnings()
        # 源网页代码
        html = response.text.encode('ISO-8859-1').decode('utf8')
        # 网页中包含章节名称及链接的数据
        content = re.findall('<dl>(.*?)</dl>', html, re.S)
        # 获取章节部分链接，缺少"https://www.xxbiquge.com"
        chapter_url_content = re.findall('<dd><a href="(.*?)">', content[0], re.S)
        # 获取章节名称
        print("正在获取章节名称")
        self.chapter_name = re.findall('">(.*?)</a>', content[0], re.S)
        print("已获取章节名称")
        # 获取章节链接，补全"https://www.xxbiquge.com"
        print("正在获取章节链接")
        for link in chapter_url_content:
            self.chapter_url.append("https://www.xxbiquge.com" + link)
        print("已获取章节链接")
        # 获取章节内容
        print("正在获取章节内容")
        for i in range(len(self.chapter_url)):
            response1 = requests.get(self.chapter_url[i])
            try:
                html1 = response1.text.encode('ISO-8859-1').decode('utf8')
                self.chapter_content.append(re.findall('<div id="content">(.*?)</div>', html1, re.S)[0])
                print("已获取第%s章内容"%self.chapter_num)
            except Exception as e:
                print("无法获取该章节内容,错误为:%s"%e)
            self.chapter_num=self.chapter_num+1
            #每隔5秒获取一次章节内容
            sleep(5)
        return self.chapter_url, self.chapter_name, self.chapter_content

    # 将章节名称及链接、内容放置到列表
    def GetChapterInfo(self):
        for i in range(len(self.chapter_content)):
            self.chapter_info.append((self.chapter_name[i], self.chapter_url[i], self.chapter_content[i]))

    # 保存数据
    def SaveNovelDataToExcel(self,NovelName,ExcelName):
        # 写入文件
        wb = openpyxl.Workbook()
        ws1 = wb.get_sheet_by_name('Sheet')
        ws1.title = NovelName
        ws1['A1'] = "章节名称"
        ws1['B1'] = "章节地址"
        ws1['C1'] = "章节内容"
        for row in self.chapter_info:
            ws1.append(row)
        wb.save("%s.xlsx"%ExcelName)

if __name__=="__main__":
    print("正在实例化对象")
    Spider=Spider_bqg_novel()
    print("正在获取章节信息")
    Spider.GetChapterData("https://www.xxbiquge.com/0_311/")
    print("正在将章节信息存入列表")
    Spider.GetChapterInfo()
    Spider.SaveNovelDataToExcel("灵域","小说2")