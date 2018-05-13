nVM=$1 		 	# the number of vms to open
insPerMin=$2 	# number of insertions per minute in the python app
maxInserts=$3 	# the python app timeout
startingIP=$4 	# the IP of vm0
batchSize=$5 	# how many insertions per batch 
rsa_key=$6

ip_components=($(echo "$startingIP" | tr '.' '\n'))

echo "$1 $2 $3 $4 $5" > args.txt

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"
	command="bash /root/Toyapp/VirtualMachines/init_VM.sh"

	scp -i $rsa_key args.txt root@$curr_IP:/root/Toyapp//Containers/Container/args.txt
	ssh -i $rsa_key root@$curr_IP $command

	((counter++))

done

rm args.txt