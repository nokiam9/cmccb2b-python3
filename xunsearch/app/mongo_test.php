<?php

$manager = new MongoDB\Driver\Manager("mongodb://mongodb:27017/");

$rp = new MongoDB\Driver\ReadPreference(MongoDB\Driver\ReadPreference::RP_PRIMARY);
$server = $manager->selectServer($rp);

var_dump($server->getInfo());

?>