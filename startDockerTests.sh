#!/bin/bash

tests_file=$1
sleep_time=$2

if [ ! -d ~/Desktop/DockerLogs/ ]; then
    mkdir ~/Desktop/DockerLogs/
fi

counter=1

cd /root/ToyApp/Containers/

while IFS='' read -r line || [[ -n "$line" ]]; do
    rm -f "~/ContainerLogs/Temp/*"
    ./start_containers.sh ${line}
    sleep ${sleep_time}
    mkdir "~/ContainerLogs/Test_"${counter}"/"
    mv "~/ContainerLogs/Temp/*" "~/ContainerLogs/Test_"${counter}"/"
    ((counter++))
done < "$tests_file"
