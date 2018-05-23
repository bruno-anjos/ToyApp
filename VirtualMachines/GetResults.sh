#!/bin/bash
startingIP=$1 	# the IP of vm0
nVM=$2 
rsa_key=$3
test=$4

ip_components=($(echo "$startingIP" | tr '.' '\n'))

if [ ! -d ~/Desktop/VMLogs/ ]; then
    mkdir ~/Desktop/VMLogs/
fi

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	echo "copying results"

	if [ ! -d ~/Desktop/VMLogs/"Test_$test" ]; then
    	    mkdir ~/Desktop/VMLogs/"Test_$test"
	fi

	scp -i $rsa_key root@$curr_IP:"/log/toyapp_log_$curr_IP" ~/Desktop/VMLogs/"Test_$test"/"VM$counter"
	echo "counter: $counter"
	((counter++))

done
