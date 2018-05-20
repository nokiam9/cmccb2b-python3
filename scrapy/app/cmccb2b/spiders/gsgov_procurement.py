# -*- coding: utf-8 -*-
import scrapy
import datetime

from cmccb2b.items import GsGovProcurementItem
from cmccb2b.utils.html2text import filter_tags, strip_non_ascii
from bson.binary import Binary
from cStringIO import StringIO

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
        li_list = response.xpath("//li[starts-with(@class, 'li')]")
        if len(li_list) == 0:
            self.logger.info(u"Find endpoint of query, and exit.")
            return

        rec = 0
        for li in li_list:
            item = GsGovProcurementItem()  # Notice: scrapy.request meta是浅复制，必须在循环内初始化class
            try:
                notice_url = li.xpath("a/@href").extract_first()
                item['nid'] = notice_url.split('/')[3].split('.')[0]
                item['title'] = li.xpath("a/text()").extract_first()

                line = li.xpath("p[1]/span/text()").extract_first().split('|')    # 第一行包含四个字段
                item['open_time'] = self.fix_open_time(line[0])  # 日期格式有多种不规范形式
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
                    url=self.domain + notice_url,
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
        """ Get context HTML from nid """
        item = response.meta['item']
        item['notice_url'] = response.url
        item['notice_content'] = filter_tags(response.body.decode('utf-8'))      # content存储公告HTML，剔除script等标签

        tag = response.xpath("//a[contains(@href, '/upload/article/')]")
        if len(tag) == 0:
            yield item
        else:
            # Notice：Mongo中的字段可以定义为数组，比标准SQL更灵活
            item['attachment'] = []
            for doc in tag:
                url = self.domain + doc.xpath("@href").extract_first()
                filename = doc.xpath('text()').extract_first()
                item['attachment'].append({
                    'url': url,
                    'filename': filename
                })
            yield scrapy.Request(
                url=item['attachment'][0]['url'],
                meta={'item': item, 'total': len(tag), 'cur': 0},
                callback=self.parse_of_attachment
            )

    def parse_of_attachment(self, response):
        """ 解析并获取公告html中包含的附件信息，利用meta传递数据实现循环的控制 """
        item = response.meta['item']
        total = response.meta['total']
        cur = response.meta['cur']

        '''mongo要求doc是utf－8格式，存储二进制文件可采用bson.binary.Binary方式，但BSON限制小于16M
        也可以采用mongo外挂的gridfs的方法，但需要手工处理doc的关联
        从性能考虑，本例不在MONGO中储存附件原文件，以下代码仅供参考'''
        # content = StringIO(response.body)
        # item['attachment'][cur]['content'] = Binary(content.getvalue())

        cur += 1
        if cur < total:
            yield scrapy.Request(
                url=item['attachment'][cur]['url'],
                meta={'item': item, 'total': total, 'cur': cur},
                callback=self.parse_of_attachment)
        else:
            yield item

    def fix_open_time(self, string):
        """ 分析字符串的内容特征，提取并返回开标日期 """
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
            self.logger.info(u"Get open_time from '{0}' failed, and reset!".format(string))
            t = datetime.datetime(1973, 2, 25)
        return t


