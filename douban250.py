"""
定义全局变量和引入包
"""
# 用来操作文件
import json
import os
# 用来发起网络请求
import time

import requests
# Python中re模块主要功能是通过正则表达式是用来匹配处理字符串的
import re

# 文件路径
res_dir = "result"
res_info_dir = "result/info"
res_comments_dir = "result/comments"
# 判断文件路径是否存在
if not os.path.exists(res_dir):
    os.mkdir(res_dir)
if not os.path.exists(res_info_dir):
    os.mkdir(res_info_dir)
if not os.path.exists(res_comments_dir):
    os.mkdir(res_comments_dir)
# 定义 TOP250 网页地址
base_url = "https://movie.douban.com/top250?start="
# 定义伪装浏览器
send_headers = {
    "Referer": "https://movie.douban.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cookie": "bid=xuMRKp9vXfQ; douban-fav-remind=1; ll=\"118173\"; __utmz=30149280.1607948606.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1607948607.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D94ADB128DB38477258690F5CB5FF1EE2|a1915678b4d1ddd64d1e906652b81d65; __utmc=30149280; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1608001308%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1474527261.1607323776.1607998283.1608001308.7; __utmb=30149280.0.10.1608001308; __utma=223695111.1351889877.1607948607.1607998283.1608001308.4; __utmb=223695111.0.10.1608001308; dbcl2=\"195748063:L5GJvVWULRo\"; ck=zzNB; _pk_id.100001.4cf6=45e370217946e0dd.1607948607.4.1608002762.1607998283.; push_noty_num=0; push_doumail_num=0"
}  # 伪装成浏览器

result_set = []

print("\n============ 开始爬取 ===========")

for i in range(0, 250, 25):
    url = base_url + str(i)
    print("正在爬取的电影列表的 url 为：", url)
    # 爬取url
    response = requests.get(url, headers=send_headers)  # 访问
    if response.status_code != 200:
        print("网络异常，或者被防火墙拦截")
        exit(1)
    print("获得的状态码为", response.status_code)
    response.encoding = "utf-8"
    response.close()
    # 访问后就关闭连接

    # 爬到的数据暂存
    res = response.text
    # 使用正则表达式匹配后存入列表 res_jj
    res_movies = re.findall('https://movie.douban.com/subject/\d+/', res)
    result_set += res_movies
    result_set = list(set(result_set))
    print("添加了25个电影", res_movies)
    # 休眠防止被封
    time.sleep(3)

with open(os.path.join(res_dir, "movie_urls.json"), 'w+', encoding='utf-8') as f:
    f.write(json.dumps(result_set))
    f.close()

# 完成第一步爬取
print("\n============ 步骤一完成 ==========="
      "\n电影列表爬取完成，获取电影列表的长度为： " + str(len(result_set)))

print("\n============ 深入爬取 ===========")

# 从之前爬取的URL列表结果集中遍历
j = 1  # 计数用
for i in result_set:
    print(i)
    # 爬取每个电影详情页中的url
    response = requests.get(i, headers=send_headers)  # 访问
    if response.status_code != 200:
        print("网络异常，或者被防火墙拦截")
        exit(1)
    print("获得的状态码为", response.status_code)
    response.encoding = "utf-8"
    response.close()
    # 访问后就关闭连接

    # 爬到的数据暂存
    res = response.text
    # 使用正则表达式匹配后存入列表
    details = re.findall('<script type="application/ld\+json">(.*?)</script>', res, flags=re.DOTALL)
    # 准备写入文件
    print("写入序号：" + str(j))
    # 处理爬取到的json换行问题
    details_str = str(details[0]).replace("\n", "")
    with open(os.path.join(res_info_dir, str(j) + ".json"), 'w+', encoding='utf-8') as f:
        f.write(details_str)
        f.close()
    print("写入电影信息完成")

    # 处理评论
    write_comments = ""
    comments = re.findall('<div class="short-content">(.*?)&nbsp;', res, flags=re.DOTALL)
    for comment in comments:
        comment = str(comment).replace(" ", "")
        comment = str(comment).replace("\n", "")
        comment = str(comment).replace("\\n", "")
        comment = str(comment).replace("<pclass=\"spoiler-tip\">", "")
        comment = str(comment).replace("</p>", "")
        write_comments = write_comments + comment + "\n"
    with open(os.path.join(res_comments_dir, str(j) + ".txt"), 'w+', encoding='utf-8') as f:
        f.write(write_comments)
        f.close()
    print("写入电影评论完成\n---------------")

    j += 1
    # 休眠防止被封
    time.sleep(5)

print("\n============ 深入爬取电影信息完成 ===========")
