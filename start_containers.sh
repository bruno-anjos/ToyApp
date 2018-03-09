#!/bin/bash

nContainers=$1
insPerMin=$2
timeout=$3
counter=0
imageName=$(cat logs/image_name.log)
command="bash init_container.sh && python3 toyapp.py $insPerMin $timeout"
echo $command

while [ $counter -lt $nContainers ]; do
	containerName="container$counter"
	echo "Starting $containerName" 
	docker run -d -it --name $containerName $imageName $command
	((counter++))
done
