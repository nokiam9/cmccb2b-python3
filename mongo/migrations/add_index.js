db = db.getSisterDB("cmccb2b");
// 主键，Scrapy.Pipeline自动创建，用于剔除重复爬取数据
db.BidNotice.createIndex(
    {'nid' : 1}, unique=true
);
// 以下查询索引，均在falsk.models中自动创建，用于Flask的列表展示，和xunsearch的增量索引
db.BidNotice.createIndex(
    {'published_date': -1, 'timestamp': -1}
);
db.BidNotice.createIndex(
    {'type_id': 1}
);
// 用于Xunsearch的增量索引刷新
db.BidNotice.createIndex(
    {'timestamp': -1}
);
printjson(db.BidNotice.getIndexes());