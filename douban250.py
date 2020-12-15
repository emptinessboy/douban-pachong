"""
定义全局变量和引入包
"""
# 用来操作文件
import json
import os
# 用来发起网络请求
import requests
# Python中re模块主要功能是通过正则表达式是用来匹配处理字符串的
import re

# 文件路径
res_dir = "result"
# 判断文件路径是否存在
if not os.path.exists(res_dir):
    os.mkdir(res_dir)
# 定义 TOP250 网页地址
base_url = "https://movie.douban.com/top250?start="
# 定义伪装浏览器
send_headers = {
    "Referer": "https://movie.douban.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9"
}  # 伪装成浏览器

result_set = []

print("\n============ 开始爬取 ===========")

for i in range(0, 250, 50):
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
    print("添加了50个电影", res_movies)

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
    print("写入文件序号：" + str(j))
    # 处理爬取到的json换行问题
    details_str = str(details[0]).replace("\n", "")
    with open(os.path.join(res_dir, str(j) + ".json"), 'w+', encoding='utf-8') as f:
        f.write(details_str)
        f.close()
    print("写入文件完成")
    j += 1
