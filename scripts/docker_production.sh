#!/bin/bash


echo "Do you have the docker image running on devlop?"
echo "Are you sure about push it to production now?"
echo "Enter 'fuck-yes' to do it: "
read user_input


if [ "$user_input" == "fuck-yes" ]; then
    echo "Continuing with the script..."

    docker tag production-app-image __bkp__production-app-image
    docker tag develop-app-image production-app-image
    
    cd ..

    sudo docker stop production-container

    docker container rm  production-container

    docker run -d --name production-container \
	-p 8000:8000 \
	-e APP_ENV=production \
	-v /home/ubuntu/persistent_data:/app/instance \
	production-app-image

    cd -

else
    echo "You didn't enter 'fuck-yes'. Exiting."
    exit 1
fi
