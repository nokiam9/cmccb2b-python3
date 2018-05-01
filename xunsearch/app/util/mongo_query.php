<?php
ini_set('display_errors','1');
error_reporting(E_ALL);

$filter = [
];

$options = [
    'limit' => 10
];

$query = new MongoDB\Driver\Query($filter, $options);

$manager = new MongoDB\Driver\Manager('mongodb://mongo:27017');
$readPreference = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
$cursor = $manager->executeQuery('cmccb2b.BidNotice', $query, $readPreference);

foreach($cursor as $document) {
    var_dump($document);
}

?>