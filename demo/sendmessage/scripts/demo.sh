#!/bin/bash

# build pybabblesdkdemo docker image
 docker build -t danu3006/pybabblesdkdemo .

# clear shell
# clear

# create and start demo container
docker run -t -i --net=babblenet --name=pybabbledemo --ip=172.77.5.5 danu3006/pybabblesdkdemo

