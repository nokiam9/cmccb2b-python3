db = db.getSisterDB("cmccb2b");
ack = db.Cmccb2bItem.updateMany(
    {'reminded_time': {'$exists': false}},
    {'$set':{'reminded_time': new Date()}},
    {muilt: true}
);
printjson(ack);