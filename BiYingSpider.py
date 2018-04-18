# -*- coding: UTF-8 -*-
_Author_ = 'Alvis'
_Date_ = '2018-04-18 15:14'

import requests
import re
import time
local = time.strftime("%Y.%m.%d")
url = 'http://cn.bing.com/'
html= requests.get(url).text
link= re.findall(u"""g_img={url: "(.*?)",""", html)
print(link)
piclink='%s%s'%(url,link[0])
print(piclink)
picture = requests.get(piclink)
with open('%s.jpg'%time.time(),'wb') as f:
    f.write(picture.content)
