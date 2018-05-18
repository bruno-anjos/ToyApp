#!/bin/bash

tests_file=$1
rsa_key=$2
sleep_time=$3

if [ ! -d ~/Desktop/DockerLogs/ ]; then
    mkdir ~/Desktop/DockerLogs/
fi

counter=0

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Executing start_vms.sh test $line"
    bash VirtualMachines/start_vms.sh ${line}
    echo "Will sleep $sleep_time"
    sleep ${sleep_time}
    echo "Executing GetResult.sh"
    IFS=' ' read -r -a array <<< "$line"
    bash VirtualMachines/GetResults.sh ${array[3]} ${array[0]} ${rsa_key} ${counter}
    ((counter++))
done < "$tests_file"