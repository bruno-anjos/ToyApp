#!/bin/bash

tests_file=$1
sleep_time=$2

counter=1

cd /root/ToyApp/Containers/

while IFS='' read -r line || [[ -n "$line" ]]; do
    rm -f "/root/ContainerLogs/Temp/*"
    ./start_containers.sh ${line}
    sleep ${sleep_time}
    mkdir "/root/ContainerLogs/Test_"${counter}
    mv "/root/ContainerLogs/Temp/*" "/root/ContainerLogs/Test_"${counter}"/"
    ((counter++))
done < "$tests_file"
