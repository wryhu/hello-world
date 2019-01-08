import requests, re
from lxml import etree
import time


def weibo(text):
    url = "https://api.weibo.com/2/statuses/share.json"
    datas = {
        "access_token":"",
        "status":"%s ‮https://www.hujie6.com" % text
    }
    file = {
        "pic":open("/home/weibo/cos.jpg", "rb")
    }
    requests.post(url=url, data=datas, files=file)

res = requests.get("https://cosplayers.global/").text
html = etree.HTML(res)
try:
    name = html.xpath('//div[@id="post_like"]//span[@class="list-name"]/text()')
except:
    name = "蜡笔小新"    
try:
    country = html.xpath('//div[@id="post_like"]//span[@class="mdl-ranking-container__flag"]/@data-balloon')
except:
    country = "阿凡达" 
pics = html.xpath('//div[@id="post_like"]//img[@class="lazy"]/@data-original')
try:
    f = open("/home/weibo/cos_id", "r")
    yesterday = f.read()
except:
    yesterday = ""
f.close()
time.sleep(1)
count = 0
for i in pics:
    id = i.split("?")[1]
    if id != yesterday:
        try:
            w = open("/home/weibo/cos_id", "w")
            w.write(id)
        except:
            pass    
        w.close()
        text = "Coser实时分享：来自%s的%s带来的作品，你知道cosplay的谁吗？" % (country[count], name[count])
        r = requests.get(i.replace("small", "large")).content
        with open('/home/weibo/cos.jpg', 'wb') as fp:
            fp.write(r)
        break
    count += 1
weibo(text)
