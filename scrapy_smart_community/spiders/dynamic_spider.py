# -*- coding: utf-8 -*-

import scrapy
import uuid

from scrapy_smart_community.items import NewsItem, NoticeItem
from scrapy_smart_community.items import ContentItem


class DynamicSpider(scrapy.Spider):
    name = "dynamic"
    start_urls = ["http://www.jnsj.net.cn/sqdt"]

    def parse(self, response):
        # 社区公告
        for notices in response.css("div#smc_tabArea2 li"):
            content_uuid = ''.join(str(uuid.uuid4()).split("-"))
            new_uuid = ''.join(str(uuid.uuid4()).split("-"))
            item_notice = NoticeItem()
            item_notice["id"] = new_uuid
            item_notice["content_id"] = content_uuid
            item_notice["title"] = notices.css('h3 a::text').extract_first()
            pub_time = notices.css("span.w-al-date::text").extract_first()
            item_notice["publish_time"] = pub_time
            href = notices.css('h3 a::attr(href)').extract_first()
            content_page = response.urljoin(href)
            self.logger.info(content_page)
            yield scrapy.Request(content_page, meta={'content_id': content_uuid, 'pub_time': pub_time}, callback=self.content_parse)
            self.logger.info(item_notice)
            yield item_notice

        # 社区新闻
        for news in response.css("div#smc_tabArea0 li"):
            content_uuid = ''.join(str(uuid.uuid4()).split("-"))
            new_uuid = ''.join(str(uuid.uuid4()).split("-"))
            item_new = NewsItem()
            item_new["id"] = new_uuid
            item_new["content_id"] = content_uuid
            item_new["title"] = news.css('h3 a::text').extract_first()
            pub_time = news.css("span.w-al-date::text").extract_first()
            item_new["publish_time"] = pub_time
            href = news.css('h3 a::attr(href)').extract_first()
            content_page = response.urljoin(href)
            self.logger.info(content_page)
            yield scrapy.Request(content_page, meta={'content_id': content_uuid, 'pub_time': pub_time}, callback=self.content_parse)
            self.logger.info(item_new)
            yield item_new

    # 内容详情
    def content_parse(self, response):
        self.logger.info(response.url)
        item_content = ContentItem()
        item_content["id"] = response.meta['content_id']
        item_content['publish_time'] = response.meta['pub_time']
        item_content["title"] = response.css("h1.w-title::text").extract_first()
        item_content["content"] = response.css("div.w-detail").extract_first()
        self.logger.info(item_content)
        yield item_content
