<?php

ini_set('display_errors','1');
error_reporting(E_ALL);

$manager = new MongoDB\Driver\Manager("mongodb://mongo:27017/");

$rp = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
$server = $manager->selectServer($rp);

var_dump($server->getInfo());

?>