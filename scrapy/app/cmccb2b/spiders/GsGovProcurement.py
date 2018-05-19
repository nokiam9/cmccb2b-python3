# -*- coding: utf-8 -*-
import scrapy
import logging, datetime

from cmccb2b.items import GsGovProcurementItem
from scrapy.exceptions import NotSupported, NotConfigured
from cmccb2b.utils.html2text import filter_tags, strip_non_ascii

logger = logging.getLogger(__name__)


class GsGovProcurementSpider(scrapy.Spider):
    name = 'GsGovProcurement'
    domain = 'http://www.gszfcg.gansu.gov.cn'
    start_url = 'http://www.gszfcg.gansu.gov.cn/web/article/128/0/index.html'

    per_page = 20
    current_page = 0
    base_query_url = 'http://www.gszfcg.gansu.gov.cn/web/doSearch.action?limit='

    def start_requests(self):  # 用start_requests()方法,代替start_urls
        """ 第一次请求一下查询页面并开启cookie，设置pre_parse回调函数使其得到cookie """
        return [scrapy.Request(
            self.start_url,
            meta={'cookiejar': 1},
            callback=self.pre_parse)]

    def pre_parse(self, response):
        """ 构造查询url，并发起Request，注意从response中获得Cookie """
        query_url = self.base_query_url + str(self.per_page) + '&start=' + str(self.per_page * self.current_page)
        logger.info(u"Start crawl url={0}".format(query_url))
        yield scrapy.Request(
            url=query_url,
            meta={'cookiejar': response.meta['cookiejar']},     # 获取响应Cookie
            callback=self.parse)

    def parse(self, response):
        """ 分析query的结果，并传入pipeline """
        # 下面的命令用于打开scrapy shell用于调试xpath
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        li_list = response.xpath("//li[starts-with(@class, 'li')]")
        if len(li_list) == 0:
            logger.info(u"Find endpoint of query, and exit.")
            return

        rec = 0
        for li in li_list:
            item = GsGovProcurementItem()  # Notice: scrapy.request meta是浅复制，必须在循环内初始化class
            try:
                notice_url = li.xpath("a/@href").extract_first()
                item['nid'] = notice_url.split('/')[3].split('.')[0]
                item['title'] = li.xpath("a/text()").extract_first()

                line = li.xpath("p[1]/span/text()").extract_first().split('|')    # 第一行包含四个字段
                item['open_time'] = self.fix_datetime(line[0])  # 日期格式有多种不规范形式
                item['published_date'] = datetime.datetime.strptime(line[1][-20:-1], '%Y-%m-%d %H:%M:%S')
                item['source_ch'] = line[2].split(u'：')[1]
                item['agency'] = line[3].split(u'：')[1]

                line = li.xpath("p[2]/span/strong/text()").extract_first().split('|') # 第一行包含3个字段
                item['notice_type'] = line[0].replace("\t", "").replace("\n", "").replace("\r", "").strip()  # 可能乱码
                item['owner'] = line[1].strip()
                item['industry'] = line[2].strip()

                item['timestamp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                logger.debug(item['title'])
            except IndexError:
                logger.warning(u'Some <li> may be empty in page %i, please check HTML as:\n%s',
                               self.current_page, li.extract())
            else:
                rec += 1
                # Get context from another parse and append field in item[]
                yield scrapy.Request(
                    url=self.domain + notice_url,
                    meta={'item': item},
                    callback=self.parse_of_content)
        logger.info(u"Current page is %i, and read %i records successful!", self.current_page, rec)

        self.current_page += 1
        query_url = self.base_query_url + str(self.per_page) + '&start=' + str(self.per_page * self.current_page)
        logger.info(u"Start crawl url={0}".format(query_url))
        yield scrapy.Request(
            url=query_url,
            meta={'cookiejar': response.meta['cookiejar']},     # 获取响应Cookie
            callback=self.parse)

    def parse_of_content(self, response):
        """ Get context HTML from nid """
        item = response.meta['item']
        item['notice_url'] = response.url
        item['notice_content'] = filter_tags(response.body.decode('utf-8'))      # content存储公告HTML，剔除script等标签
        yield item

    def fix_datetime(self, string):
        """ 分析字符串的内容特征，提取日期信息并返回 """
        year, month, day, hour, minute, second = 0, 0, 0, 0, 0, 0
        words = strip_non_ascii(string).strip(' ').split(' ')  # 剔除中文字符，去除头尾空格，按中间空格分为date,time

        try:
            if words[0].find('/') > 0:
                d = words[0].split('/')
            else:
                d = words[0].split('-')
            year = int(d[0])
            month = int(d[1])
            day = int(d[2])

            if len(words) > 1:
                t = words[1].split(":")
                hour = int(t[0])
                minute = int(t[1])
                if len(t) > 2:
                    second = int(t[2])
            t = datetime.datetime(year, month, day, hour=hour, minute=minute, second=second)
        except (IndexError, UnicodeEncodeError, ValueError):
            logger.info(u"Get open_time from '{0}' failed, and reset!".format(string))
            t = datetime.datetime(1973, 2, 25)
        return t


