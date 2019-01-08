from selenium import webdriver
import time
import re
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def weibo(text):
    url = "https://api.weibo.com/2/statuses/share.json"
    datas = {
        "access_token":"",
        "status":"%s ‮https://www.hujie6.com" % text
    }
    file = {
        "pic":open("/home/weibo/guojia.jpg", "rb")
    }
    requests.post(url=url, data=datas, files=file)

cap = DesiredCapabilities.PHANTOMJS.copy()
cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.5.2.18321'
driver = webdriver.PhantomJS(executable_path = "/usr/local/bin/phantomjs", desired_capabilities=cap)
driver.get("http://www.ngchina.com.cn/photography/photo_of_the_day/")
time.sleep(20)
html = driver.page_source
item = re.findall(r'"imgs" href="(.+?)"', html)[0]
url = "http://www.ngchina.com.cn" + item
driver.get(url)
time.sleep(5)
result = driver.page_source
pic_url = re.findall(r'###"><img src="(.+?)"', result)[0]
try:
	profile = re.findall(r'article_con"><div>(.+?)</', result)[0]
except:
	profile = "分享世界"	
try:
	name = re.findall(r'(摄影：.+?)，', result)[0]
except:
	name = "分享世界"	
text = "[ 国家地理杂志 ]%s\n%s" % (profile, name)
cookies = driver.get_cookies()
headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.5.2.18321"
}
cookie_value = ""
for item in cookies:
	if "yjs_ab_lid" in [x for x in item.values()]:
		cookie_value += "yjs_ab_lid=%s; " % item['value']
	elif "yjs_ab_score" in [x for x in item.values()]:
		cookie_value += "yjs_ab_score=%s; " % item['value']
	elif "__cfduid" in [x for x in item.values()]:
		cookie_value += "__cfduid=%s; " % item['value']
	elif "cf_clearance" in [x for x in item.values()]:
		cookie_value += "cf_clearance=%s; " % item['value']			
headers["Cookie"] = cookie_value
r = requests.get(pic_url, headers=headers).content
with open('/home/weibo/guojia.jpg', 'wb') as fp:
    fp.write(r)
weibo(text)
driver.close()
