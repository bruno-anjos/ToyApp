startingIP=$1 	# the IP of vm0
nVM=$2 	# how many insertions per batch 
rsa_key=$3

ip_components=($(echo "$startingIP" | tr '.' '\n'))
mkdir ~/Desktop/VMLogs

counter=0 
while [ $counter -lt $nVM ]; do

	last_component=$((${ip_components[3]} + counter))
	curr_IP="${ip_components[0]}.${ip_components[1]}.${ip_components[2]}.${last_component}"

	echo "copying results"
	scp -i $rsa_key root@$curr_IP:"/log/toyapp_log_$curr_IP" ~/Desktop/VMLogs/"VM$counter"
	
	echo "counter: $counter"
	((counter++))

done

rm args.txt