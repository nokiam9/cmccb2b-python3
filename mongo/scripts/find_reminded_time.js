db = db.getSisterDB("cmccb2b");
ack = db.Cmccb2bItem.find(
    {'reminded_time': {'$exists': false}}
    ).count()
print("matched record counts=" + ack);