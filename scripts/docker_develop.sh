#!/bin/bash

cd ..

sudo docker stop develop-container

docker container rm  develop-container

sudo docker build --no-cache -t develop-app-image .

docker run -d --name develop-container \
    -p 8001:8000 \
    -e APP_ENV=development \
    -v /home/ubuntu/persistent_data:/app/instance \
    develop-app-image

cd -

