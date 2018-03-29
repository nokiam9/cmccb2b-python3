var i=0;
var j=0;
var db = db.getSisterDB("cmccb2b");

db.Cmccb2bItem.find().forEach(
    function(x) {
        // print(x.title);
        // print(x.crawled_time);
        var t0 = new Date(x.crawled_time);
        x.crawled_time = new Date(t0.getTime() + 8 * 60 * 60 * 1000);
        // print(x.crawled_time);
        i += 1;
        if (x.reminded_time) {
            // print("\t" + x.reminded_time)
            t0 = new Date(x.reminded_time);
            x.reminded_time = new Date(t0.getTime() + 8 * 60 * 60 * 1000);
            // print("\t" + x.reminded_time)
            j += 1;
        }
        db.Cmccb2bItem.save(x);
        print("crawled_time update count:" + i + ", crawled_time update count:" + j)
    }
)

print("Matched crawled_time records=" + i +".");
print("Matched reminded_time records=" + j + ".")
