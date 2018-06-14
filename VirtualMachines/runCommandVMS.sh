#!/bin/bash

nVM=$1		 	# the number of vms to open
startingIP=$2 	# the IP of vm0
rsa_key=$3
command=$4

ip_components=($(echo "$startingIP" | tr '.' '\n'))


counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	echo "running ${command} on ${curr_IP}"

	ssh -i $rsa_key root@$curr_IP $command

	((counter++))

done