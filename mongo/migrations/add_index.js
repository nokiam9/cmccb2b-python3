db = db.getSisterDB("cmccb2b");
// 用于Flask的列表展示排序
db.BidNotice.createIndex(
    {'published_date': -1, 'timestamp': -1}
    );
// 主键，用于ScrapyPipeline剔除重复爬取数据
db.BidNotice.createIndex(
    {'nid' : 1}, unique=true
    );
db.BidNotice.createIndex(
    {'type_id': 1}
    );
// 用于Xunsearch的增量索引刷新
db.BidNotice.createIndex(
    {'timestamp': -1}
    );
// db.BidNotice.createIndex(
//     {'notice_type': 1}
//     );
printjson(db.BidNotice.getIndexes());