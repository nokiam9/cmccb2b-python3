# -*- coding: utf-8 -*-
import scrapy
import datetime

from cmccb2b.items import BidNoticeItem
from scrapy.exceptions import NotSupported, CloseSpider
from cmccb2b.utils.html2text import filter_tags


class HQSupplierNoticeSpider(scrapy.Spider):
    name = 'HQSupplierNotice'
    domain = 'https://b2b.10086.cn'

    query_url = 'https://b2b.10086.cn/b2b/main/showSupplier.html'
    base_content_url = 'https://b2b.10086.cn/b2b/main/viewVendorNoticeContent.html?noticeBean.id=' # +id(int)

    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/68.0.3440.106 Mobile Safari/537.36',
    }

    def start_requests(self):  # 用start_requests()方法,代替start_urls
        """ 首先请求查询列表页面，并回调到pre_parse """
        self.current_page = 1
        self.page_size = 20
        self.form_data = {
            'page.currentPage': str(self.current_page),
            'page.perPageSize': str(self.page_size),
            'noticeBean.companyType': 'hq',  # or 'province,professional'
            'noticeBean.companyName': '',
            'noticeBean.title': '',
            'noticeBean.startDate': '',
            'noticeBean.endDate': ''
        }
        return [scrapy.FormRequest(
            url=self.query_url,
            formdata=self.form_data,
            headers=self.base_headers,
            callback=self.parse)]

    def parse(self, response):
        """ 读取Ajax的HTML内容，并提取列表信息 """
        try:
            table = response.xpath("//table")[0]
        except IndexError:
            self.logger.error(u"Can't find <table> in page %i, this spider abort! response=\n%s",
                              self.current_page, response.body)
            raise CloseSpider("html_format_error")

        rec = 0
        for tr in table.xpath("tr[position() > 2]"):
            item = BidNoticeItem()          # Notice: scrapy.request meta是浅复制，必须在循环内初始化class
            try:
                item['spider'] = self.name          # 伪数据:'BidNotice' 

                item['type_id'] = '99'              # 伪数据
                nid = tr.xpath("@onclick").extract_first().split('\'')[1]
                item['nid'] =  str(99000000 + int(nid))     # 伪id，99000000+id

                item['notice_type'] = tr.xpath("td[1]/text()").extract_first()
                item['source_ch'] = '总部'        # 本query的数据只有3列，手工填写
                item['title'] = tr.xpath("td[2]/a/text()").extract_first()

                published_date = tr.xpath("td[3]/text()").extract_first()
                item['published_date'] = datetime.datetime.strptime(published_date, '%Y-%m-%d')

                # Set timestamp with UTC＋8hours
                item['timestamp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            except IndexError:
                self.logger.warning(u'Some <td> may be empty in page %i, please check HTML as:\n%s',
                                    self.current_page, tr.extract())
            else:
                rec += 1
                # Get context from another parse and append field in item[]
                yield scrapy.Request(
                    url=self.base_content_url + nid,
                    headers=self.base_headers,
                    meta={'item': item},
                    callback=self.parse_of_content
                )

        if rec == 0:
            self.logger.info(u"Find the end of query and close spider now! current page is %i.", self.current_page)
            return

        self.logger.info(u"Current page is %i, and read %i records successful!", self.current_page, rec)
        if rec % self.page_size == 0:
            self.current_page += rec // self.page_size
        else:
            self.current_page += rec // self.page_size + 1

        # Notice: formdata fields must be str, int type will occur yield failed!!
        self.form_data['page.currentPage'] = str(self.current_page)
        yield scrapy.FormRequest(
            url=self.query_url,
            formdata=self.form_data,
            headers=self.base_headers,
            callback=self.parse
        )

    def parse_of_content(self, response):
        """ 解析，并存储公告HTML文本 """
        item = response.meta['item']
        item['notice_url'] = response.url
        item['notice_content'] = filter_tags(response.body.decode('utf-8'))      # HTML剔除script等标签

        # 解析html，并以数组方式保存附件文件信息
        item['attachment_urls'] = []
        for doc in response.xpath("//a[contains(@href, '/b2b/main/commonDownload.html?')]"):
            url = self.domain + doc.xpath("@href").extract_first()
            description = doc.xpath('font/text()').extract_first()
            item['attachment_urls'].append({
                'url': url,
                'description': description
            })
        yield item
