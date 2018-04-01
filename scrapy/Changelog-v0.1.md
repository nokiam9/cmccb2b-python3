###  scrapy v0.1 on 201804 ###

#### 开发记录  ####
- 现在是基于python3.6的开发
- scrapy提供`run.py`的手工启动方式，但docker scrapy仍然采用基于curl调用的启动方式
- 调整`run.py`位置到`app/`，原来放在spider的目录会影响scrapyd的启动
- 重写`Cmccb2bPipeline`，改造为与item无关的基础库，并基于`settings.py`进行配置
- 解决mongo不支持timezone，导致order by时无法按本地时间排序的问题，处理方法是修改了timestamp的数据定义，
_现在mongo DB实际上存储的是"错误的UTC时间"_
- 相应的，增加`mongo/migrations/transfer_utctime_plus_8hours.js`，py方式的参考脚本在workspace/， 并更新了基础样本数据
- 修复递归调用request时item数据混乱的bug，处理方法是将spider中item()初始化调整到循环体的内部，因为scrapy.request的meta传递是浅复制
- 修改collection的定义，现在是`cmccb2b.bid_notices`，并将字段`crawled_time`修改为`timestamp`,增加了字段`notice_context`


#### 经验之谈 ####
- `pipelines.py`还有目前无法解决的bug，raise exception无效导致deffer异常退出。scrapy仅支持NotConfigure异常，不支持自定义的异常，
open_spider时发现mongo连接失败，或create index失败时，因为spider尚未打开，也无法close_spider, pipelines直接就放弃）

#### 后续任务 ####
- `pipelines.py`发现bug，不支持unique key的列表方式，
修改方式参见[scrapy-mongodb](https://github.com/nokiam9/scrapy-mongodb/blob/master/scrapy_mongodb.py)
- 考虑mail的开发基于extension，支持sensitive_words的搜索，问题是无法直接调用pipeline的mongo连接
- 因为数据量太大，context尚未启用，考虑过滤context的html标签，仅存储文字


