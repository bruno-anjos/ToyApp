#!/bin/bash

tests_folder=$1

#AVERAGE LOOP
IFS='
'

counter=0
first="teste"
for line in `cat ${tests_folder}/* | grep Average`; do
    IFS=' ' read -r -a array <<< "$line"
    if [ ${counter} -eq 0 ]; then
        first=${array[4]}
    elif [[ ${array[4]} != ${first} ]]; then
        echo "Found different averages on counter ${counter}"
        exit 1
    fi

    ((counter++))
done

echo "Averages are the same"

#ROW COUNT LOOP
counter=0
first="teste"
for line in `cat ${tests_folder}/* | grep Row`; do
    IFS=' ' read -r -a array <<< "$line"
    if [ ${counter} -eq 0 ]; then
        first=${array[3]}
    elif [[ ${array[3]} != ${first} ]]; then
        echo "Found different row counts on counter ${counter}"
        exit 1
    fi

    ((counter++))
done

echo "Row counts are the same"

#CREATE CSV
echo "Creating CSV..."
echo "IP, Sync, Ran, DeSync" > ${tests_folder}/test.csv

for file in ${tests_folder}/toyapp*; do
    lines=$(head -5 "${file}")
    IFS=$'\n' read -rd '' -a lineArray <<<"${lines}"
    IFS=' ' read -r -a ip <<< "${lineArray[0]}"
    IFS=' ' read -r -a sync <<< "${lineArray[1]}"
    IFS=' ' read -r -a ran <<< "${lineArray[2]}"
    IFS=' ' read -r -a desync <<< "${lineArray[3]}"
    echo "${ip[3]}, ${sync[1]}, ${ran[2]}, ${desync[3]}" >> ${tests_folder}/test.csv
done

echo "CSV created at ${tests_folder}/test.csv"