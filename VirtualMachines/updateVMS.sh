#!/bin/bash

nVM=$1		 	# the number of vms to open
startingIP=$2 	# the IP of vm0
rsa_key=$3
toCopy=$4


counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	echo "copying args to: $curr_IP"

	scp -i $rsa_key -r $toCopy root@$curr_IP:~/

	((counter++))

done