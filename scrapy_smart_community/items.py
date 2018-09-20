# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # 咨询表id
    id = scrapy.Field()
    # 资讯类型
    tab_id = scrapy.Field()
    # 内容 id
    content_id = scrapy.Field()
    # 标题 （冗余查询）
    title = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()


class NoticeItem(scrapy.Item):
    # 咨询表id
    id = scrapy.Field()
    # 资讯类型
    tab_id = scrapy.Field()
    # 内容 id
    content_id = scrapy.Field()
    # 标题 （冗余查询）
    title = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()


class ContentItem(scrapy.Item):
    # 内容表id
    id = scrapy.Field()
    # 新闻标题
    title = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # 发布时间 （冗余查询）
    publish_time = scrapy.Field()



