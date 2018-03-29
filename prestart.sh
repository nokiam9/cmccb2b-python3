#!/usr/bin/env bash

# Create docker network
docker network create frontend_net
docker network create backend_net

# Prepare mongo container for develop
docker-compose -f mongo/mongo.yml -f mongo/mongo.override.yml up -d

# Prepare mongo container for runtime
## docker-compose -f mongo/mongo.yml up -d
