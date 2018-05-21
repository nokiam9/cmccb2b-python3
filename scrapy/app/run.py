# coding:utf-8

from scrapy import cmdline


cmdline.execute('scrapy crawl BidNotice -a type_id=2 --loglevel=INFO '.split())
# cmdline.execute('scrapy crawl GsGovProcurement --loglevel=INFO '.split())
