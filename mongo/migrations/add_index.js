db = db.getSisterDB("cmccb2b");
db.BidNotice.createIndex(
    {'published_date': -1, 'timestamp': -1}
    );
db.BidNotice.createIndex(
    {'id' : 1}, unique=true
    );
db.BidNotice.createIndex(
    {'type_id': 1}
    );
db.BidNotice.createIndex(
    {'notice_type': 1}
    );
printjson(db.BidNotice.getIndexes());