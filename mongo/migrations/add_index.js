db = db.getSisterDB("cmccb2b");
db.BidNotice.createIndex(
    {'published_date': -1, 'timestamp': -1}
    );
printjson(db.BidNotice.getIndexes());