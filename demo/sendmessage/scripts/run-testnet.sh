#!/bin/bash

set -eux

N=${1:-4}
MPWD=$(pwd)
PPADDR="172.77.5.254:1338" #Proxy publish address

docker network create \
  --driver=bridge \
  --subnet=172.77.0.0/16 \
  --ip-range=172.77.5.0/24 \
  --gateway=172.77.5.254 \
  babblenet

# publish node1 proxy address on the host machine
docker create --name=node1 --net=babblenet --ip=172.77.5.1 mosaicnetworks/babble:0.2.1 run \
--cache_size=50000 \
--tcp_timeout=200 \
--heartbeat=10 \
--node_addr="172.77.5.1:1337" \
    --proxy_addr="172.77.5.1:1338" \
    --client_addr="172.77.5.5:1339" \
    --service_addr="172.77.5.1:80" \
    --sync_limit=500 \
    --store="inmem"
    docker cp $MPWD/conf/node1 node1:/.babble
    docker start node1

for i in $(seq 2 $N)
do
    docker create --name=node$i --net=babblenet --ip=172.77.5.$i mosaicnetworks/babble:0.2.1 run \
    --cache_size=50000 \
    --tcp_timeout=200 \
    --heartbeat=10 \
    --node_addr="172.77.5.$i:1337" \
    --proxy_addr="172.77.5.$i:1338" \
    --service_addr="172.77.5.$i:80" \
    --sync_limit=500 \
    --store="inmem"
    docker cp $MPWD/conf/node$i node$i:/.babble
    docker start node$i
done
