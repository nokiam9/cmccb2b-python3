# -*- coding: utf-8 -*-
import scrapy
import logging
import datetime

from cmccb2b.items import BidNoticeItem
from scrapy.exceptions import NotSupported, NotConfigured

from cmccb2b.utils.html2text import filter_tags

logger = logging.getLogger(__name__)


class BidNoticeSpider(scrapy.Spider):
    name = 'bid_notice'

    def __init__(self, type_id, *args, **kwargs):
        """
        Construct
        :param notice_type: scrapy crawl $spider -a type_id=?
                1:单一来源采购公告
                2:采购公告(default value)
                3:资格预审公告
                4:N/A，测试是2015年的数据，似乎已经被废弃
                5:N/A
                6:N/A
                7:招标结果公示
                8:供应商信息收集公告
                9:N/A
        """
        super(BidNoticeSpider, self).__init__(*args, **kwargs)

        self.type_id = str(int(type_id))
        if self.type_id not in ['1', '2', '3', '7', '8']:
            logger.error(u"Unsupported type_id with {0} and abort!!!".format(type_id))
            raise NotSupported
        else:
            logger.info(u"Set crawler argument with type_id={0}".format(self.type_id))

        self.query_url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=' \
                         + str(self.type_id)
        self.context_url = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='  # append with id(int)

        self.current_page = 1
        self.page_size = 20
        self.form_data = {
            'page.currentPage': str(self.current_page),
            'page.perPageSize': str(self.page_size),
            'noticeBean.sourceCH': '',
            'noticeBean.source': '',
            'noticeBean.title': '',
            'noticeBean.startDate': '',
            'noticeBean.endDate': ''
        }

    def start_requests(self):
        """ Start crawler """
        return [scrapy.FormRequest(
            url=self.query_url,
            formdata=self.form_data,
            callback=self.parse
        )]

    def parse(self, response):
        """ Parse """
        try:
            table = response.xpath("//table")[0]
        except IndexError:
            logger.error(u"Can't find <table> in page %i, this spider abort! response=\n%s",
                         self.current_page, response.body)
            raise CloseSpider("html_format_error")
        # -------------------------------------------------------------
        # - Get <tr> and bypass top 2 line for table head
        # - In Python program, default use unicode string, when dump file, just write value as memory.
        #   if you cannot read chinese word, check it as  .decode('unicode-escape')
        # - In Python, time() always locate in UTC Zone 0, 8 hours before PEK.
        # - Instead of scrapy.log(), Scrapy 1.4 use scrapy.logger(), which is based on python log system logging.log().
        #   log error with 5 levels: critical, error, warning, info, debug
        # - bid notice ID 64996, source_ch is empty, due to fix error!!!
        # -------------------------------------------------------------
        rec = 0
        for tr in table.xpath("tr[position() > 2]"):
            item = BidNoticeItem()          # Notice: scrapy.request meta是浅复制，必须在循环内初始化class
            try:
                item['type_id'] = self.type_id
                item['nid'] = tr.xpath("@onclick").extract_first().split('\'')[1]
                item['source_ch'] = tr.xpath("td[1]/text()").extract_first()
                item['notice_type'] = tr.xpath("td[2]/text()").extract_first()
                item['title'] = tr.xpath("td[3]/a/text()").extract_first()

                # Transfer $published_date from string to datetime
                published_date = tr.xpath("td[4]/text()").extract_first()
                item['published_date'] = datetime.datetime.strptime(published_date, '%Y-%m-%d')

                # Set timestamp with UTC＋8hours
                item['timestamp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            except IndexError:
                logger.warning(u'Some <td> may be empty in page %i, please check HTML as:\n%s',
                               self.current_page, tr.extract())
            else:
                rec += 1
                # Get context from another parse and append field in item[]
                yield scrapy.Request(
                      url=self.context_url+str(item['nid']),
                      meta={'item': item},
                      callback=self.parse_of_context)

        if rec == 0:
            logger.info(u"Find the end of query and close spider now! current page is %i.", self.current_page)
            return

        logger.info(u"Current page is %i, and read %i records successful!", self.current_page, rec)
        if rec % self.page_size == 0:
            self.current_page += rec // self.page_size
        else:
            self.current_page += rec // self.page_size + 1

        # Notice: formdata fields must be str, int type will occur yield failed!!
        self.form_data['page.currentPage'] = str(self.current_page)
        yield scrapy.FormRequest(
            url=self.query_url,
            formdata=self.form_data,
            callback=self.parse
        )

    def parse_of_context(self, response):
        """ Get context HTML from nid """
        item = response.meta['item']
        item['notice_url'] = response.url
        item['notice_content'] = filter_tags(response.body.decode('utf-8'))      # content存储公告HTML，剔除script等标签
        yield item
