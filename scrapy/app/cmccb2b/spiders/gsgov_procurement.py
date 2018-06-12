# -*- coding: utf-8 -*-
import scrapy
import datetime

from cmccb2b.items import GsGovProcurementItem
from cmccb2b.utils.html2text import filter_tags, strip_non_ascii


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
        self.logger.info(u"Start crawl url={0}".format(query_url))
        yield scrapy.Request(
            url=query_url,
            meta={'cookiejar': response.meta['cookiejar']},     # 获取响应Cookie
            callback=self.parse)

    def parse(self, response):
        """ 分析query的结果，并传入pipeline """
        tag = response.xpath("//li[starts-with(@class, 'li')]")
        if len(tag) == 0:
            self.logger.info(u"Find endpoint of query, and exit.")
            return

        rec = 0
        for li in tag:
            item = GsGovProcurementItem()  # Notice: scrapy.request meta是浅复制，必须在循环内初始化class
            try:
                notice_path = li.xpath("a/@href").extract_first()
                item['spider'] = self.name
                item['nid'] = notice_path.split('/')[3].split('.')[0]
                item['title'] = li.xpath("a/text()").extract_first()

                line = li.xpath("p[1]/span/text()").extract_first().split('|')    # 第一行包含四个字段
                item['open_time'] = _fix_open_time(line[0])     # 日期格式有多种不规范形式
                item['published_date'] = datetime.datetime.strptime(line[1][-20:-1], '%Y-%m-%d %H:%M:%S')
                item['source_ch'] = line[2].split(u'：')[1]
                item['agency'] = line[3].split(u'：')[1]

                line = li.xpath("p[2]/span/strong/text()").extract_first().split('|')   # 第一行包含3个字段
                item['notice_type'] = line[0].replace("\t", "").replace("\n", "").replace("\r", "").strip()  # 可能有乱码
                item['owner'] = line[1].strip()
                item['industry'] = line[2].strip()

                item['timestamp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                self.logger.debug(item['title'])
            except IndexError:
                self.logger.warning(u'Some <li> may be empty in page %i, please check HTML as:\n%s',
                                    self.current_page, li.extract())
            else:
                rec += 1
                # Get context from another parse and append field in item[]
                yield scrapy.Request(
                    url=self.domain + notice_path,
                    meta={'item': item},
                    callback=self.parse_of_content)
        self.logger.info(u"Current page is %i, and read %i records successful!", self.current_page, rec)

        self.current_page += 1
        query_url = self.base_query_url + str(self.per_page) + '&start=' + str(self.per_page * self.current_page)
        self.logger.info(u"Start crawl url={0}".format(query_url))
        yield scrapy.Request(
            url=query_url,
            meta={'cookiejar': response.meta['cookiejar']},     # 获取响应Cookie
            callback=self.parse)

    def parse_of_content(self, response):
        """ 解析html文本，找出并存储附件信息｛url: description｝ """
        item = response.meta['item']
        item['notice_url'] = response.url
        item['notice_content'] = filter_tags(response.body.decode('utf-8'))      # content存储公告HTML，剔除script等标签

        item['attachment_urls'] = []
        for doc in response.xpath("//a[contains(@href, '/upload/article/')]"):
            url = self.domain + doc.xpath("@href").extract_first()
            description = doc.xpath('text()').extract_first()
            item['attachment_urls'].append({
                'url': url,
                'description': description
            })
        yield item


def _fix_open_time(self, string):
    """ 分析字符串的内容特征，提取并返回开标日期, 如果格式错误，返回1970/1/1 """
    year, month, day, hour, minute, second = 0, 0, 0, 0, 0, 0
    words = strip_non_ascii(string).strip(' ').split(' ')  # 剔除中文字符，去除头尾空格，按中间空格分为date,time

    try:
        year, month, day = map(int, words[0].split('-'))
    except ValueError:
        try:
            year, month, day = map(int, words[0].split('/'))
        except ValueError:
            return datetime.datetime.utcfromtimestamp(0)

    if len(words) > 1:
        try:
            hour, minute, second = map(int, words[1].split(':'))
        except ValueError:
            try:
                second = 0
                hour, minute = map(int, words[1].split(':'))
            except ValueError:
                return datetime.datetime.utcfromtimestamp(0)

    try:
        return datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        return datetime.datetime.utcfromtimestamp(0)



