# -*- coding: utf-8 -*-

# Scrapy settings for cmccb2b project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cmccb2b'

SPIDER_MODULES = ['cmccb2b.spiders']
NEWSPIDER_MODULE = 'cmccb2b.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cmccb2b (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False          # ignore scrapy limited setting of website

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cmccb2b.middlewares.Cmccb2BSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'cmccb2b.middlewares.Cmccb2BDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'cmccb2b.pipelines.Cmccb2bPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Defined for scrapy mongodb
# URI: mongodb://[username:password@]host1[:port1],...[,hostN[:portN]]][/[database][?options]]
MONGODB_URI = 'mongodb://mongo:27017'       # 必须的，默认值mongodb://localhost:27017
MONGODB_DATABASE = 'cmccb2b'                # 必须的，数据库名称
MONGODB_COLLECTION = 'bid_notices'          # 必须的，表空间名称

# MONGODB_SEPARATE_COLLECTIONS =            # 未启用，支持每个spider插入不同的collection
MONGODB_UNIQUE_KEY = 'id'                   # 可选的，定义唯一索引：'id', 或［('id', 1), ('title', -1)］
MONGODB_STOP_ON_DUPLICATE = 10              # 可选的，＝0：不会停止爬取，<0：报错退出

# Todo: Define for scrapy.mail
MAIL_FROM = '13901214002@139.com'           #
MAIL_HOST = 'smtp.139.com'		    	    # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
MAIL_PORT = 465                             # 25-SMTP, 465-SMTPS（SMTP-over-SSL）
MAIL_USER = '13901214002@139.com'		    # 发件人的用户名
MAIL_PASS = 'eos5d3'			            # 密码
MAIL_TLS = True                             # 强制使用STARTTLS
MAIL_SSL = True                             # 强制使用SSL加密连接

