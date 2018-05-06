#!/usr/bin/env php
<?php
require_once '/app/xunsearch-sdk/php/lib/XS.php';

define("XS_PROJECT", "cmccb2b");
define("XS_UPDATE_LOG" , "cmccb2b.xunsearch_update_log");
define("MONGO_SOURCE", "cmccb2b.BidNotice");
define("MONGO_URI", "mongodb://mongo:27017");

// 打开错误输出，release时关闭
ini_set('display_errors','1');
error_reporting(E_ALL);
// 强制指定编码，防止浏览器显示乱码
header("Content-type:text/html;charset=utf-8");

// 加载XS LIB，并取得index和document
$index=connect_index();
$manager=connect_mongodb();

// Start to update index
$start_time = get_UTCTime();

// Update index
$last = get_last_timestamp($manager);
$records=update_index($manager, $index, $last);

// Save log for increment update
$stop_time = get_UTCTime();
set_last_timestamp($manager, $start_time, $stop_time, $records);

// 立即刷新index
echo "Flush index and log...", PHP_EOL;
$index->flushIndex();
$index->flushLogging();

echo "End of xs_update.php", PHP_EOL;


function set_last_timestamp($manager, $start_time, $stop_time, $records) {
    $tz0 = new \MongoDB\BSON\UTCDateTime();
    $now = new \MongoDB\BSON\UTCDateTime((double)(string)$tz0 + 8*60*60*1000); # TimeZone No.9

    $bulk = new MongoDB\Driver\BulkWrite;
    $document = [
        'project' => XS_PROJECT,
        'source' => MONGO_SOURCE,
        'start_time' => $start_time,
        'end_time' => $stop_time,
        'update_records' => $records,
    ];
    $_id1 = $bulk->insert($document);
    $result = $manager->executeBulkWrite(XS_UPDATE_LOG, $bulk);
    echo "Saving update index log.", PHP_EOL;
    var_dump($document);

    return $result;
}

function get_last_timestamp($manager) {
    $filter =['project'=>XS_PROJECT];
    $options = ['sort' => ['start_time'=> -1]];
    $query = new MongoDB\Driver\Query($filter, $options);

    $readPreference = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
    $cursor = $manager->executeQuery(XS_UPDATE_LOG, $query, $readPreference);

    $ret = $cursor->toArray();
    if (count($ret) > 0) {
        echo "Get max start-time from Mongo DB ={$ret[0]->start_time->toDatetime()->format('Y-m-d H:i:s')}" , PHP_EOL;
        return $ret[0]->start_time;
    }
    echo "Update log empty, reset to 0 and reindex all!!!", PHP_EOL;
    return 0;
}

function connect_index() {
    $xs = new XS(XS_PROJECT);    // 自动使用 $prefix/sdk/php/app/demo.ini 作项目配置文件
    $index = $xs->index;        // 获取 索引对象
    return $index;
}

function connect_mongodb() {
    $manager = new MongoDB\Driver\Manager(MONGO_URI);
    return $manager;
}

function update_index($mongo_manager, $index, $last_time) {
    // 在cursor的循环中，取得field数据，并转换格式加载到XS
    $filter = array(
        'timestamp' => array(
            '$gte' => $last_time,
        ),
    );
    $options = [
    //    'limit' => 10
    ];
    $query = new MongoDB\Driver\Query($filter, $options);

    $readPreference = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
    $cursor = $mongo_manager->executeQuery(MONGO_SOURCE, $query, $readPreference);

    $count = 1;
    $document = new XSDocument;
    foreach($cursor as $record) {
        $document->setField('nid', $record->id);                         // mongo目前设置为str类型，
        $document->setField('title', $record->title);
        $document->setField('source_ch', $record->source_ch);
        $document->setField('notice_context', $record->notice_context);  // TODO：计划将纯字符文本，改为剔除script等标签的html
        // UTCDateTime被转换为(int)20180920,用于搜索结果的时间排序，注意：忽略His，因为实际数据只精确到日期，
        $document->setField('published_date', (int)$record->published_date->toDatetime()->format("Ymd"));
        $document->setField('timestamp', $record->timestamp->toDatetime()->format('Y-m-d H:i:s'));

        $ret = $index->update($document);
        // var_dump($record->published_date);
//        echo "Update index {$count}: {$record->timestamp->toDatetime()->format('Y-m-d H:i:s')}, {$record->title}.", PHP_EOL;
        echo "Update index {$count}: {$document->f('title')}.", PHP_EOL;
        $count += 1;
    }
    return $count;
}

function get_UTCTime() {
    $tz0 = new \MongoDB\BSON\UTCDateTime();
    $now = new \MongoDB\BSON\UTCDateTime((double)(string)$tz0 + 8*60*60*1000); # TimeZone No.9
    return $now;
}

?>
