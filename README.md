### Python爬虫

大数据分析处理的首要步骤就是获取 原始数据集，这里的过程我编写了一个简单的python程序来实现数据的
采集和初步的处理 。完整代码见附件。

**使用的工具：**

PyCharm Python3.9 Chrome开发者工具

**爬取电影详情页地址列表：**

在爬取前，我先初步分析了豆瓣网的源代码，进行初步爬取方案的制订。经过浏览豆瓣 T op 250 电影列表，
我得出了豆瓣网的电影列表每页显示的数目为 25 条，并且可以通过URL参数start来进行控制。

例如获取前 25 条电影数据：https://movie.douban.com/top250?start=

25 条到第 50 条：https://movie.douban.com/top250?start=

因此我只需要让Python程序按照 25 的步长遍历URL的start参数，再使用正则表达式匹配每个电影具体的
URL就可以获得Top 250 每部电影的详情地址。

**模块代码：**

[![image015.png](https://media.everdo.cn/tank/pic-bed/2021/03/01/image015.png)](https://up.media.everdo.cn/image/oNkL)

[![image016.png](https://media.everdo.cn/tank/pic-bed/2021/03/01/image016.png)](https://up.media.everdo.cn/image/okwc)

[![image017.png](https://media.everdo.cn/tank/pic-bed/2021/03/01/image017.png)](https://up.media.everdo.cn/image/o9n2)

这部分爬取完成后，我将数据序列化后写入 文件movie_urls.json，最后得到了如下的电影详情地址列表：

[![image018.png](https://media.everdo.cn/tank/pic-bed/2021/03/01/image018.png)](https://up.media.everdo.cn/image/ocTk)

[![image019.png](https://media.everdo.cn/tank/pic-bed/2021/03/01/image019.png)](https://up.media.everdo.cn/image/oEQZ)

#### 爬取每个电影的具体详情：

爬取这部分数据前，我通过开发者工具查看源代码，发现豆瓣电影详情页中，电影名称，导演，演员，年份等大量的信息都是通过JavaScript进行渲染输出的。而原始数据就存在网页中一段脚本中。

而我要做的就是先遍历访问之前爬取 得到的电影详情列表中的每一个链接地址， 然后使用正则表达式提取这部分我需要的内容 。而针对制片国家 等其他 的信息， 则通过寻找DOM树的方式，使用正则表达式匹配对应的标签后进行爬取。

#### 模块代码：





这部分爬取完成后，我没有额外处理 数据，直接将数据 按照一个电影一个文件的方式存放到了 250 个json
中，其中文件名就是电影的排名。这里我先不清洗数据，将数据清洗的过程留给后面的MapReduce来进行
处理。其中爬取得到的数据大致如下。


#### 爬取每个电影的前十条评论：

最后我再使用同样的方式爬取每部电影下面的十条评论，按照一行一个的格式存到了对应的1- 250的txt文
本文件中。

#### 爬取过程：

#### 爬取过程截图如下


#### 遇到的问题和反爬虫策略的解决：

#### IP被封

#### 在爬取的过程中豆瓣禁封了我的网络IP地址导致爬取中途出错的情况。

对于这个问题，我尝试在request模块添加了自己登陆后的cookie作为请求头，实测添加头后豆瓣立刻放行
了我的爬虫程序。

```
send_headers = {
"Referer": "https://movie.douban.com/",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/87.0.4280.88 Safari/537.36",
"Accept":
"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-
exchange;v=b3;q=0.9",


"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "我的cookie"
}
```

账号被封
在添加完自己的登录信息后，正常爬取到 100 多条数据后，再次出现错误。这次网页的提示是我的账户被临
时禁封了。

经过排查。是由于我的请求频次过快导致。再给每个request请求加上指定的sleep秒数后，再次尝试爬取，
就可以顺利完成爬取过程了。