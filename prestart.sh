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
docker network create frontend_net
docker network create backend_net

if test ${mode} = 1 ; then
    docker-compose -f mongo/mongo.yml -f mongo/mongo.override.yml up -d
else
    docker-compose -f mongo/mongo.yml up -d
fi

