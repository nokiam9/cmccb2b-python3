db=db.getSisterDB('cmccb2b');
print("now DB=", db.getName());
print("all collections are:");
print(db.getCollectionNames());
print("BidNotice record count=",db.BidNotice.count());