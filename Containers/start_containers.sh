#!/bin/bash
docker rm -f $(docker ps -a -q)  # removes all containers
docker volume prune -f


nContainers=$1 # the number of containers to open
insPerMin=$2 # number of insertions per minute in the python app
maxInserts=$3 # the python app timeout
startingIP=$4 #the IP of Container0
batchSize=$5 #how many insertions per batch 

imageName=$(cat logs/image_name.log) # fetches the image name in the logs file
command="bash init_container.sh $insPerMin $maxInserts $nContainers $startingIP $batchSize" # built command to pass to the container
counter=0 

while [ $counter -lt $nContainers ]; do
	containerName="Container$counter" 
	echo "Starting $containerName"
	docker run -d --mount type=tmpfs,destination=/var/lib/mysql,tmpfs-mode=0777 -v ~/Desktop/ContainerLogs:/log --name $containerName $imageName $command
	((counter++))
done
