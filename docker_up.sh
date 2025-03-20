#!/bin/bash

docker build -t ros2-xtendtask:latest .
xhost +local:docker
docker run -it \
    --env DISPLAY=$DISPLAY \
    --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
    ros2-xtendtask:latest
