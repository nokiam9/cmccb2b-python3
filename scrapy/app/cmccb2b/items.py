# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class NoticeBaseItem(scrapy.Item):      # 各类招标信息的公共基类，包含必须的字段信息
    spider = scrapy.Field()
    nid = scrapy.Field()                # Primary Key
    source_ch = scrapy.Field()
    notice_type = scrapy.Field()
    title = scrapy.Field()
    published_date = scrapy.Field()
    notice_url = scrapy.Field()
    notice_content = scrapy.Field()     # HTML文本，剔除了<script>等无效标签内容
    attachment = scrapy.Field()         # 可能的数组，包含附件文件的url和filename
    timestamp = scrapy.Field()
    files_urls = scrapy.Field()
    files = scrapy.Field()
    images_urls = scrapy.Field()
    images = scrapy.Field()


class BidNoticeItem(NoticeBaseItem):       # cmccb2b招标公告
    type_id = scrapy.Field()


class GsGovProcurementItem(NoticeBaseItem):    # 甘肃政府采购网
    owner = scrapy.Field()
    open_time = scrapy.Field()
    agency = scrapy.Field()
    industry = scrapy.Field()


