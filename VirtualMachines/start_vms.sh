insPerMin=$1 	# number of insertions per minute in the python app
maxInserts=$2 	# the python app timeout
nVM=$3		 	# the number of vms to open
startingIP=$4 	# the IP of vm0
batchSize=$5 	# how many insertions per batch 
rsa_key=$6

ip_components=($(echo "$startingIP" | tr '.' '\n'))

echo "$1 $2 $3 $4 $5" > args.txt

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	command="cd Toyapp/VirtualMachines && bash init_VM.sh"

	echo "copying args to: $curr_IP"
	scp -i $rsa_key args.txt root@$curr_IP:Toyapp/Containers/Container/args.txt
	echo "Starting app on: $curr_IP"
	ssh -i $rsa_key root@$curr_IP $command
#screen -d -m 
	((counter++))

done

rm args.txt