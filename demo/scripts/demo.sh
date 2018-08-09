#!/bin/bash

# clear shell
clear

# build demo for test purposes
docker build -t moasicnetworks/pybabblesdkdemo .

# define four client nodes
N=${1:-4}

for i in $(seq 1 ${N})
do
    docker run -t -i -d --net=babblenet --name=demo${i} --ip=172.77.5.$((${N} + ${i})) moasicnetworks/pybabblesdkdemo:latest \
        --nodehost 172.77.5.${i} \
        --nodeport 1338 \
        --listenhost 172.77.5.$((${N} + ${i})) \
        --listenport 1339
done

docker attach demo1