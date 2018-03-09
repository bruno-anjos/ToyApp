#!/bin/bash

nContainers=$1 # the number of containers to open
insPerMin=$2 # number of insertions per minute in the python app
timeout=$3 # the python app timeout
imageName=$(cat logs/image_name.log) # fetches the image name in the logs file
command="bash init_container.sh $insPerMin $timeout" # built command to pass to the container
counter=0 

while [ $counter -lt $nContainers ]; do
	containerName="Container$counter" 
	echo "Starting $containerName" 
	docker run -d  --name $containerName $imageName $command
	((counter++))
done
