import re

import requests

url = "https://movie.douban.com/subject/33420285/comments?status=P"

headers = {
    'Referer': 'https://movie.douban.com/subject/33420285/comments?status=P',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

response = requests.get("https://movie.douban.com/subject/1291546/", headers=headers)  # 访问
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
title = re.findall('<script type="application/ld\+json">(.*?)</script>', res, flags=re.DOTALL)
# title = re.findall('<script type="application/ld\+json">([\s\S]*?)</script>', res)
# title = re.search('<script type="application/ld\+json">.*</script>', res, flags=re.DOTALL)
print(title[0])
