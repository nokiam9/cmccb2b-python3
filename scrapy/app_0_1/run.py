# coding:utf-8

from scrapy import cmdline


cmdline.execute('scrapy crawl bid_notice --loglevel=INFO '.split())
cmdline.execute('scrapy crawl notice_result --loglevel=INFO '.split())
cmdline.execute('scrapy crawl single_source_procurement --loglevel=INFO '.split())
