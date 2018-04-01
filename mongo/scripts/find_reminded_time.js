db = db.getSisterDB("cmccb2b");
ack = db.BidNotice.find(
    {'reminded_time': {'$exists': false}}
    ).count()
print("matched record counts=" + ack);