#!/bin/bash

rm -r -f logs #removes previous logs
mkdir logs #creates a new directory to store logs
touch logs/install_log.log #creates a new log file
touch logs/image_name.log #creates a log to have the image name

echo "Building Docker image"
docker build Container > logs/install_log.log # redirects all output to the logs file
cat logs/install_log.log | grep "Successfully built" #just displays the success message

#does some magic stuff to get the image name into the file "image_name"
cat logs/install_log.log | grep "Successfully built" > logs/image_name.log
perl -pi -e 's/Successfully built//g' logs/image_name.log
perl -pi -e 's/ //g' logs/image_name.log


