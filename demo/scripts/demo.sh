#!/bin/bash

# clear shell
clear

# build demo for test purposes
docker build -t mosaicnetworks/pybabblesdkdemo .

# define four client nodes
N=${1:-4}

# run 4 sendmessage apps with dynamic ips and
for i in $(seq 1 ${N})
do
    docker run -t -i -d --net=babblenet --name=demo${i} --ip=172.77.5.$((${N} + ${i})) mosaicnetworks/pybabblesdkdemo:latest \
        --nodehost 172.77.5.${i} \
        --nodeport 1338 \
        --listenhost 172.77.5.$((${N} + ${i})) \
        --listenport 1339
done