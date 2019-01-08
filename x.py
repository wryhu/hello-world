import requests
import re
import time


def weibo(text):
    url = "https://api.weibo.com/2/statuses/share.json"
    datas = {
        "access_token":"",
        "status":"%s https://www.hujie6.com" % text
    }
    file = {
        "pic":open("/home/weibo/cook.jpg", "rb")
    }
    requests.post(url=url, data=datas, files=file)


res = requests.get("http://www.xiachufang.com/activity/site/?order=pop").text
id = re.findall(r'data-id="(\d+?)"', res)[0]
time.sleep(10)
res2 = requests.get("http://www.xiachufang.com/dish/%s/" % id).text
pic_url = re.findall(r't="(http:.+?)"', res2)[0]
try:
    name = re.findall(r'】(.+?)_', res2)[0]
except:
    name = "蜡笔小新"
try:
    mes = re.findall(r'ption" content="(.+?)"', res2, re.DOTALL)[0].replace("#", "_")
    if len(mes) > 120:
        mes = mes[:120]
except:
    mes = "哦依稀"
try:
    pic_time = re.findall(r'拍摄</a>于(.+?)<', res2, re.DOTALL)[0].strip()[11:]
except:
    pic_time = "今日" 
text = "%s：\n%s\n拍摄于%s" % (name, mes, pic_time)
time.sleep(5)
r = requests.get(pic_url).content
with open('/home/weibo/cook.jpg', 'wb') as fp:
    fp.write(r)
weibo(text)
