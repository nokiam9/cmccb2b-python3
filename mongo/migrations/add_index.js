db = db.getSisterDB("cmccb2b");
db.BidNotice.createIndex(
    {'published_date': -1, 'timestamp': -1}
    );
db.BidNotice.createIndex(
    {'id' : 1}, unique=true
    );
printjson(db.BidNotice.getIndexes());