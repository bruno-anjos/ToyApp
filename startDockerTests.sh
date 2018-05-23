#!/bin/bash

tests_file=$1
rsa_key=$2
sleep_time=$3
ip=10.170.138.198

if [ ! -d ~/Desktop/DockerLogs/ ]; then
    mkdir ~/Desktop/DockerLogs/
fi

counter=0

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Deleting container logs..."
    ssh -n -i $rsa_key root@$ip rm -f "~/Desktop/ContainerLogs/*"
    echo "Starting test $line"
    command="cd ToyApp/Containers/ && ./start_containers.sh $line"
    screen -d -m -L ssh -i $rsa_key root@$ip $command
    echo "Will sleep $sleep_time"
    sleep $sleep_time
    mkdir ~/Desktop/DockerLogs/"Test_$counter"
    echo "Downloading logs to ~/Desktop/DockerLogs/"Test_$counter"/"
    scp -i $rsa_key root@$ip:~/Desktop/ContainerLogs/* ~/Desktop/DockerLogs/"Test_$counter"/ < /dev/null
    ((counter++))
done < "$tests_file"
