#!/bin/bash

tests_file=$1
sleep_time=$2

counter=1
mkdir /root/ContainerLogs/
cd /root/ToyApp/Containers/

while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "Starting test $counter... args: $line"

    rm -f /root/Desktop/ContainerLogs/*
    ./start_containers.sh ${line}

    echo "sleeping...."
    sleep ${sleep_time}
    mkdir /root/ContainerLogs/Test_${counter}

    mv /root/Desktop/ContainerLogs/* /root/ContainerLogs/Test_${counter}/

    echo "Test $counter done"
    ((counter++))
done < "$tests_file"
