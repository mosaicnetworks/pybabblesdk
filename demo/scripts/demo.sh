#!/bin/bash

# clear shell
clear

# create and start demo container
docker run -t -i --net=babblenet --name=pybabbledemo --ip=172.77.5.5 moasicnetworks/pybabblesdkdemo

