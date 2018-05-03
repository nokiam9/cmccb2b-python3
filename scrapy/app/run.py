# coding:utf-8

from scrapy import cmdline


cmdline.execute('scrapy crawl bid_notice -a type_id=2 --loglevel=INFO '.split())