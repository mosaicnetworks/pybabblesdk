#!/bin/bash

set -eux

N=${1:-4}
MPWD=$(pwd)

docker network create \
    --driver=bridge \
    --subnet=172.77.0.0/16 \
    --ip-range=172.77.5.0/24 \
    --gateway=172.77.5.254 \
    babblenet


for i in $(seq 1 $N)
do
    docker create --name=node$i --net=babblenet --ip=172.77.5.$i mosaicnetworks/babble:0.2.1 run \
    --cache_size=50000 \
    --tcp_timeout=200 \
    --heartbeat=10 \
    --node_addr="172.77.5.$i:1337" \
    --client_addr="172.77.5.$(($N+$i)):1339" \
    --proxy_addr="172.77.5.$i:1338" \
    --service_addr="172.77.5.$i:80" \
    --sync_limit=500 \
    --store="inmem"
    docker cp $MPWD/conf/node$i node$i:/.babble
    docker start node$i
done
