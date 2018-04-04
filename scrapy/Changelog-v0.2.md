###  scrapy v0.2 on 201804 ###

#### 开发记录  ####
- 修改`scrapy/pipelines.py`，支持设置SEPARATE_COLLECTIONS，主要功能是根据spider.name设置collection
- 新增`scrapy/notice_result.py`，爬取招标结果的信息，并存入`cmccb2b.notice_result`表空间
- 更名`scrapy/bidnotice.py`为`scrapy.bid_notice.py`，保持一致的命名规则
- 调整`scrapy/settings.py`的相应参数设置

#### 待办任务  ####
- 将`scrapy.bidnotice`更名为`scrapy.bid_notice`，并相应更改了collection名字，需要修改相关的script和shell