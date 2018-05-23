#!/bin/bash
insPerMin=$2 	# number of insertions per minute in the python app
maxInserts=$3 	# the python app timeout
nVM=$1		 	# the number of vms to open
startingIP=$4 	# the IP of vm0
batchSize=$5 	# how many insertions per batch 
rsa_key=$6

args_file="args.txt"

ip_components=($(echo "$startingIP" | tr '.' '\n'))

echo "$2 $3 $1 $4 $5" > $args_file

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	command="cd ToyApp/VirtualMachines && bash init_VM.sh"

	echo "copying args to: $curr_IP"
	scp -i $rsa_key $args_file root@$curr_IP:~/ToyApp/Containers/Container/args.txt
	echo "Starting app on: $curr_IP"
	screen -d -m -L ssh -i $rsa_key root@$curr_IP $command

	((counter++))

done

rm args.txt

