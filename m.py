import requests
from PIL import Image
import re
import time
import os

def weibo(text):
    url = "https://api.weibo.com/2/statuses/share.json"
    datas = {
        "access_token":"",
        "status":"%s https://www.hujie6.com" % text
    }
    file = {
        "pic":open("/home/weibo/manga/manga.jpg", "rb")
    }
    requests.post(url=url, data=datas, files=file)

res = requests.get("https://www.pixiv.net/ranking.php?mode=daily&content=manga").text
pics = re.findall(r'(https://i.pximg.net/c.+?.jpg)', res)
try:
    items = re.findall(r'data-rank-text="(.+?)" data-title="(.+?)" data-user-name="(.+?)".+?id="(\d+?)"', res)
except:
    items = [["100位", "哦呼", "蜡笔小新", "111"], ["100位", "哦呼", "蜡笔小新", "111"], ["100位", "哦呼", "蜡笔小新", "111"],]

count = 0
with open("/home/weibo/manga_id", "r+") as f:
    yesterday = f.read()
    for i in items:
        id = i[3]
        if id not in yesterday:
            f.write(id+"\n")
            item = items[count]
            text = "漫画分享：p站今日排名第%s的画师「 %s 」的作品< %s >。作品id：%s" % (item[0], item[2], item[1], id)
            pic_url = pics[count].replace("/c/240x480", "")
            try:
                page = int(re.findall(r'<span>(\d{0,2})</span>', res)[count])
            except:
                page = 2
            os.chdir(r'/home/weibo/manga')
            headers = {'referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % id}
            for i in list(range(page)):
                pic = pic_url.replace("p0", "p%d" % i)
                pic_name = str(i)
                r = requests.get(url=pic, headers=headers).content
                with open(pic_name, 'wb') as fp:
                    fp.write(r)
                time.sleep(5)
            ims = [Image.open(pict) for pict in os.listdir()]
            width, height = ims[0].size
            result = Image.new(ims[0].mode, (width, height*len(ims)))
            for i, p in enumerate(ims):
                result.paste(p, box=(0, i*height))
            result.save('manga.jpg') 
            break
        count += 1
weibo(text)
for i in os.listdir():
    os.remove(i)
