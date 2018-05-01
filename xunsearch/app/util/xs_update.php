<?php
// 打开错误输出，release时关闭
ini_set('display_errors','1');
error_reporting(E_ALL);

// 强制指定编码，防止浏览器显示乱码
header("Content-type:text/html;charset=utf-8");

//加载XS LIB，并取得index和document
require_once '/app/xunsearch-sdk/php/lib/XS.php';
$xs = new XS('cmccb2b');    // 自动使用 $prefix/sdk/php/app/demo.ini 作项目配置文件
$index = $xs->index;        // 获取 索引对象
$doc = new XSDocument;

//连接mongodb，设置并执行query，取得cursor
$filter = [
];

$options = [
    'limit' => 1100
];
$query = new MongoDB\Driver\Query($filter, $options);

$manager = new MongoDB\Driver\Manager('mongodb://mongo:27017');
$readPreference = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
$cursor = $manager->executeQuery('cmccb2b.BidNotice', $query, $readPreference);

//在cursor的循环中，取得field数据，并转换格式加载到XS
foreach($cursor as $record) {
    $doc->setField('nid', $record->id);
    $doc->setField('title', $record->title);
    $doc->setField('source_ch', $record->source_ch);
    $doc->setField('notice_context', $record->notice_context);
    $doc->setField('published_date', 0);

    $ret = $index->update($doc);
    echo "Update index for document title={$record->title}...<br>";
//    var_dump($ret);
}

$index.flush();

?>
