db=db.getSisterDB('cmccb2b');
print("now DB=", db.getName());
print("all collections are:");
print(db.getCollectionNames());
print("Cmccb2bItem record count=",db.Cmccb2bItem.count());