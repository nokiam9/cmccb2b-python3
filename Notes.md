- scrapy的spider打开shell用于调试xpath的方法 
```python
from scrapy.shell import inspect_response
inspect_response(response, self)
```

- normalize-space()的功能是去掉前后的空格。xpath函数normalize-space的两种用法.

第一种方法非常实用,normalize-space用在属性上，如  
`response.xpath("//div[normalize-space(@class)='nav']/text()")`

第二种方法：normalize-space用结果上，如  
`response.xpath("normalize-space（//div[normalize-space(@class)='nav']/text()）")`

- 提取html所有文本的最简单方法   
`response.xpath("string(.)")
`