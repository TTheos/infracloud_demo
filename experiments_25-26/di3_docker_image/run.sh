#!/bin/bash

IMAGE=di3-image
CONTAINER=di3-running

docker rm -f $CONTAINER 2>/dev/null
docker build -t $IMAGE .
docker run -d -p 8080:8080 --name $CONTAINER $IMAGE

echo "Container running:"
docker ps | grep $CONTAINER

echo "Test with curl:"
curl http://127.0.0.1:8080
