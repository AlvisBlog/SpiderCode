#coding=utf8
_Author_ = 'Alvis'
_Date_ = '2018-04-29 20:56'

import re
import requests
import openpyxl
qd_url='https://www.qidian.com/'
response=requests.get(qd_url)
html=response.text.encode('ISO-8859-1').decode('utf8')
all_type=re.findall('<span class="info"><i>(.*?)</i>',html,re.S)
all_type_num=re.findall('</i><b>(.*?)</b>',html,re.S)
all_type_url=re.findall('href="/(.*?)"',re.findall('<dl>(.*?)</dl>',html,re.S)[0],re.S)
all_type_info=[]
for i in range(len(all_type)):
    all_type_info.append((all_type[i],all_type_num[i],"https://www.qidian.com/"+all_type_url[i]))
del all_type_info[12]
print(all_type_info)