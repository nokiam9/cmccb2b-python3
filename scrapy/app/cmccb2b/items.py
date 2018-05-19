# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class BidNoticeItem(scrapy.Item):       # cmccb2b招标公告
    nid = scrapy.Field()
    source_ch = scrapy.Field()
    notice_type = scrapy.Field()
    title = scrapy.Field()
    published_date = scrapy.Field()
    timestamp = scrapy.Field()

    notice_url = scrapy.Field()
    notice_content = scrapy.Field()
    type_id = scrapy.Field()


class GsGovProcurementItem(scrapy.Item):    # 甘肃政府采购网
    nid = scrapy.Field()        # PrimaryKey，设置为html文件名
    source_ch = scrapy.Field()
    notice_type = scrapy.Field()
    title = scrapy.Field()
    published_date = scrapy.Field()
    notice_url = scrapy.Field()
    notice_content = scrapy.Field()
    timestamp = scrapy.Field()

    owner = scrapy.Field()
    open_time = scrapy.Field()
    agency = scrapy.Field()
    industry = scrapy.Field()


