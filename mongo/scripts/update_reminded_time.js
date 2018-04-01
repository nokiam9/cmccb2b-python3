db = db.getSisterDB("cmccb2b");
ack = db.BidNotice.updateMany(
    {'reminded_time': {'$exists': false}},
    {'$set':{'reminded_time': new Date()}},
    {muilt: true}
);
printjson(ack);