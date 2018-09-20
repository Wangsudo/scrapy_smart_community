# scrapy_smart_community
使用scrapy爬取了一个社区的门户网页的新闻，公告信息。

## 环境
macos 10.13

pyton 2.7.5

scrapy 1.5.1

mysql Ver 14.14 Distrib 5.7.19

## 实现功能
1. 资讯 递归 爬取 （已完成）
  
2. 爬取资讯 分别 入库 （已完成）

3. 图片下载，上传oss （待开发）

4. 去重url爬取 （待开发：目前只是简单进行入库去重，可以利用redis进行分布式去重url爬取）

## 运行
首先 运行环境要有 scrapy  
下载scrapy (可能要升级 pip，按照提示升级pip) 
```
pip install scrapy
```

clone下项目
```
git clone ~~~~~~~~~
```
修改setting.py文件下的数据库配置

进入 scrapy_smart_community 文件夹下
```
scrapy crawl dynamic
```

## 定时运行
这里介绍
使用 crontab

```
crontal -e
```
在vi中写类似如下crontab的指令：
30 17 * * * cd [项目路径] && /usr/local/bin/scrapy crawl xxx

## 博客详解
（待总结）
