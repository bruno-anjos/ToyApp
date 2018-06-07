#!/bin/bash
startingIP=$1 	# the IP of vm0
nVM=$2 
rsa_key=$3
installer=$4

ip_components=($(echo "$startingIP" | tr '.' '\n'))

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	echo "Installing dependencies"

	scp -i $rsa_key $installer root@$curr_IP:~
	screen -d -m -L ssh -i $rsa_key root@$curr_IP bash $installer

	echo "counter: $counter"
	((counter++))

done