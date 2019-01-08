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
        "pic":open("/home/weibo/pixiv.jpg", "rb")
    }
    requests.post(url=url, data=datas, files=file)

res = requests.get("https://www.pixiv.net/ranking.php?mode=daily&content=illust").text
pics = re.findall(r'(https://i.pximg.net/c.+?.jpg)', res)
try:
    items = re.findall(r'data-rank-text="(.+?)" data-title="(.+?)" data-user-name="(.+?)".+?id="(\d+?)"', res)
except:
    items = [["100位", "哦呼", "蜡笔小新", "111"], ["100位", "哦呼", "蜡笔小新", "111"], ["100位", "哦呼", "蜡笔小新", "111"],]
count = 0
with open("/home/weibo/illust_ids", "r+") as f:
    yesterday = f.read()
    for i in items:
        id = i[3]
        if id not in yesterday:
            f.write(id+"\n")
            item = items[count]
            text = "插画分享：p站今日排名第%s的画师「 %s 」的作品< %s >。作品id：%s" % (item[0], item[2], item[1], id)
            pic_url = pics[count].replace("/c/240x480", "")
            headers = {'referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % id}
            time.sleep(10)
            r = requests.get(url=pic_url, headers=headers).content
            with open('/home/weibo/pixiv.jpg', 'wb') as fp:
                fp.write(r)
            break
        count += 1
weibo(text)
