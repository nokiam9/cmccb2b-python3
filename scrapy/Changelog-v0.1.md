###  scrapy v0.1 on 201804 ###

#### 开发记录  ####
- `Cmccb2bPipeline`已经成为与item无关的基础库（通过`settings.py`配置实现）,
但还存在raise exception无效导致deffer异常退出的bug（scrapy仅支持NotConfigure异常，不支持自定义的异常）
- scrapy现在提供run.py的启动方式
- 将spider中item()初始化调整到循环体的内部，因为scrapy.request的meta传递是浅复制，可能造成多进程的数据不一致的bug
- collection的名字修改为`cmccb2b.bid_notices`，并将字段`crawled_time`修改为`timestamp`,增加了字段`notice_context`


#### TODO ####
- mail extension的开发，支持sensitive_words的搜索
- 因为数据量太大，context尚未启用，考虑过滤context的html标签，仅存储文字

------
#### 解决json.dump不支持datetime类型的问题 ####
```python
import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), cls=DateEncoder) + "\n"
        self.file.write(line.encode('utf-8'))
        return item
```
