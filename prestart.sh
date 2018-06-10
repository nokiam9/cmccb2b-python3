#!/usr/bin/env bash

mode=0
if [ -z "$1" ]; then
    echo "no arg, start with default runtime mode"
else
    case $1 in
    '-dev') echo "start with develop mode......"
        mode=1
    ;;
    '-run') echo "start with runtime mode......"
    ;;
    *) echo "undefined arg, use default runtime mode"
    ;;
    esac
fi

# Create docker network
docker network create cmccb2b_net

if test ${mode} = 1 ; then
    docker-compose -f mongo/mongo.yml -f mongo/mongo.override.yml up -d
else
    docker-compose -f mongo/mongo.yml up -d
fi

# Create indexes of collection
# echo "Create indexes of cmccb2b.BidNotice..."
# sleep 5
# docker exec -it mongo mongo /data/migrations/add_index.js


