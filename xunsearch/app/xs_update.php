#!/usr/bin/env php
<?php
// 打开错误输出，release时关闭
ini_set('display_errors','1');
error_reporting(E_ALL);

// 强制指定编码，防止浏览器显示乱码
header("Content-type:text/html;charset=utf-8");

$TIMESTAMP_INTERVAL = 24*60*60*1000;     # 设置刷新索引的间隔时间，默认是24小时

// 加载XS LIB，并取得index和document
require_once '/app/xunsearch-sdk/php/lib/XS.php';
$xs = new XS('cmccb2b');    // 自动使用 $prefix/sdk/php/app/demo.ini 作项目配置文件
$index = $xs->index;        // 获取 索引对象
$doc = new XSDocument;

// 连接mongodb，设置并执行query，取得cursor
$tz0 = new \MongoDB\BSON\UTCDateTime();
$now = new \MongoDB\BSON\UTCDateTime((double)(string)$tz0 + 8*60*60*1000); # TimeZone No.9
//echo 'now2 = ', $now->toDatetime()->format('Y-m-d H:i:s'), PHP_EOL;

$last = new \MongoDB\BSON\UTCDateTime((double)(string)$now - $TIMESTAMP_INTERVAL);
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

// 在cursor的循环中，取得field数据，并转换格式加载到XS
$count = 1;
foreach($cursor as $record) {
    $doc->setField('nid', $record->id);                         // mongo目前设置为str类型，
    $doc->setField('title', $record->title);
    $doc->setField('source_ch', $record->source_ch);
    $doc->setField('notice_context', $record->notice_context);  // TODO：计划将纯字符文本，改为剔除script等标签的html
    // UTCDateTime被转换为(int)20180920,用于搜索结果的时间排序，注意：忽略His，因为实际数据只精确到日期，
    $doc->setField('published_date', (int)$record->published_date->toDatetime()->format("Ymd"));
    $doc->setField('timestamp', $record->timestamp->toDatetime()->format('Y-m-d H:i:s'));

    $ret = $index->update($doc);
    // var_dump($record->published_date);
    echo "Update index ", $count, ": {$record->title}.", PHP_EOL;
    $count += 1;
}

// 立即刷新index
//$index.flush();

?>
