#!/bin/bash

docker build -t project .
cd user-interface
docker build -t app .
cd ../
docker-compose up
