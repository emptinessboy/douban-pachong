import json
import re

import requests

url = "https://movie.douban.com/subject/33420285/comments?status=P"

headers = {
    "Referer": "https://movie.douban.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cookie": "bid=xuMRKp9vXfQ; douban-fav-remind=1; ll=\"118173\"; __utmz=30149280.1607948606.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1607948607.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D94ADB128DB38477258690F5CB5FF1EE2|a1915678b4d1ddd64d1e906652b81d65; __utmc=30149280; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1608001308%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1474527261.1607323776.1607998283.1608001308.7; __utmb=30149280.0.10.1608001308; __utma=223695111.1351889877.1607948607.1607998283.1608001308.4; __utmb=223695111.0.10.1608001308; dbcl2=\"195748063:L5GJvVWULRo\"; ck=zzNB; _pk_id.100001.4cf6=45e370217946e0dd.1607948607.4.1608002762.1607998283.; push_noty_num=0; push_doumail_num=0"
}

response = requests.get("https://movie.douban.com/subject/1292052/", headers=headers)  # 访问
if response.status_code != 200:
    print("网络异常，或者被防火墙拦截")
    exit(1)
print("获得的状态码为", response.status_code)
response.encoding = "utf-8"
response.close()
# 访问后就关闭连接

# 爬到的数据暂存
res = response.text
# res = res.replace("@", "")
# 使用正则表达式匹配后存入列表 res_jj
comments = re.findall('<div class="short-content">(.*?)&nbsp;', res, flags=re.DOTALL)
for comment in comments:
    # comment = str(comment).replace(" ", "")
    comment = "".join(comment.split())
    comment = str(comment).replace("\n", "")
    comment = str(comment).replace("\\n", "")
    comment = str(comment).replace("<pclass=\"spoiler-tip\">", "")
    comment = str(comment).replace("</p>", "")
    print(comment.split(" "))

# comments = json.load(json.dumps(comments))
# for comment in comments:
#     print(comment)
# title = re.findall('<script type="application/ld\+json">([\s\S]*?)</script>', res)
# title = re.search('<script type="application/ld\+json">.*</script>', res, flags=re.DOTALL)

