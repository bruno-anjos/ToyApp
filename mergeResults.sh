#!/usr/bin/env bash

logs_folder=$1
filterResultsPath=$2

rm ${logs_folder}/merged_results.csv
total=0

for folder in ${logs_folder}/*/; do
    echo "Filtering results for folder ${folder}"
    ${filterResultsPath} ${folder}
    ((total++))
done

cd $logs_folder
counter=1
while [ $counter -lt $total ]; do
	file=Test_$counter/test.csv
    echo "Merging ${file} with ${logs_folder}merged_results.csv..."
    cat $file >> $logs_folder/merged_results.csv
    printf "\n" >> $logs_folder/merged_results.csv
    ((counter++))
done