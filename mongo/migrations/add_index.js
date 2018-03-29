db = db.getSisterDB("cmccb2b");
db.Cmccb2bItem.createIndex(
    {'published_date': -1, 'crawled_time': -1}
    );
printjson(db.Cmccb2bItem.getIndexes());