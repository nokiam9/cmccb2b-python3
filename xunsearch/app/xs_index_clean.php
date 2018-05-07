#!/usr/bin/env php
<?php
// 打开错误输出，release时关闭
ini_set('display_errors','1');
error_reporting(E_ALL);
// 强制指定编码，防止浏览器显示乱码
header("Content-type:text/html;charset=utf-8");

require_once '/app/xunsearch-sdk/php/lib/XS.php';

define("XS_PROJECT", "cmccb2b");
define("XS_UPDATE_LOG" , "cmccb2b.XunsearchUpdateLog");
define("MONGO_SOURCE", "cmccb2b.BidNotice");
define("MONGO_URI", "mongodb://mongo:27017");

$xs = new XS(XS_PROJECT);    // 自动使用 $prefix/sdk/php/app/demo.ini 作项目配置文件
$indexer = $xs->index;        // 获取 索引对象
$indexer->clean();
echo "Clean index ......";

$manager = new MongoDB\Driver\Manager(MONGO_URI);
$command = new MongoDB\Driver\Command([
    'drop' => 'XunsearchUpdateLog'
]);

try {
    $cursor = $manager->executeCommand('cmccb2b', $command);
} catch(MongoDB\Driver\Exception $e) {
    echo $e->getMessage(), "\n";
    exit;
}

echo "Drop update log in MongoDB ......";

?>