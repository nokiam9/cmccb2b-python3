#!/usr/bin/env bash

php /app/util/mongo_query.php | /app/xunsearch-sdk/php/util/Indexer.php -p cmccb2b --source=json
