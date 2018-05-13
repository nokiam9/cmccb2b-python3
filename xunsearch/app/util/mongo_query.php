#!/usr/bin/env php
<?php
ini_set('display_errors','1');
error_reporting(E_ALL);

// 强?~H??~L~G?~Z?~V?| ~A?~L?~X?止?~O?~H?~Y??~X?示乱?| ~A
header("Content-type:text/html;charset=utf-8");

$tz0 = new \MongoDB\BSON\UTCDateTime();
$now = new \MongoDB\BSON\UTCDateTime((double)(string)$tz0 + 8*60*60*1000); # TimeZone No.9
//echo 'now2 = ', $now->toDatetime()->format('Y-m-d H:i:s'), PHP_EOL;

$last = new \MongoDB\BSON\UTCDateTime((double)(string)$now - 5*60*1000);
//echo 'last2 = ', $last->toDatetime()->format('Y-m-d H:i:s'), PHP_EOL;

$filter = array(
    'timestamp' => array(
        '$gte' => $last,
        '$lt'  => $now,
    ),
);

$options = [
//    'limit' => 10
];

$query = new MongoDB\Driver\Query($filter, $options);

$manager = new MongoDB\Driver\Manager('mongodb://mongo:27017');
$readPreference = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
$cursor = $manager->executeQuery('cmccb2b.BidNotice', $query, $readPreference);

foreach($cursor as $doc) {
    $arr = array(
        "nid" => $doc->nid,
        "title" => $doc->title,
        "source_ch" => $doc->source_ch,
        "published_date" => (int)$doc->published_date->toDatetime()->format("Ymd"),
        "timestamp" => $doc->timestamp->toDatetime()->format('Y-m-d H:i:s'),
        "notice_context" => $doc->notice_content,
    );
    echo json_encode($arr), PHP_EOL;
}

//[nid]
//[title]
//[source_ch]
//[published_date]
//[timestamp]
//[notice_context]

?>