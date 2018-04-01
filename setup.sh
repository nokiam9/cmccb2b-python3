#!/usr/bin/env bash

# Git clone && pre setup.sh
:<<eof
apt update
apt install git
cd /
git clone https://github.com/nokiam9/cmccb2b_runtime.git
mv cmccb2b_runtime app
cd /app
sh setup.sh
eof

echo "Install docker......"
suodo apt update
sudo apt install docker.io

echo "Install docker-compose......"
sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

echo "Install mongo client......"
sudo apt install mongodb-clients

echo "Install gzip......"
sudo apt install gzip

echo "Prepare UserData ......"
cd /app
mkdir UserData
mkdir UserDdata/db UserData/logs

echo "Prepare environment for start......"
sh prestart.sh

echo "Migration mongo db data......"
cd /app/utils/migrations
cat BidNotice.json.sample.gz| gzip -d | mongoimport -d cmccb2b -c BidNotice --drop
mongo add_index.js

echo "Start docker package......"
docker-compose up -d --build