#!/bin/bash

cd ..

docker container rm -f your-flask-app-container
sudo docker build -t your-flask-app-image .
sudo docker run -d --name your-flask-app-container -p 8000:8000 your-flask-app-image

cd -

