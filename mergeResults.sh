#!/usr/bin/env bash

tests_folder=$1
filterResultsPath=$2

rm ${tests_folder}/merged_results.csv
total=0

for folder in ${tests_folder}/*/; do
    echo "Filtering results for folder ${folder}"
    ${filterResultsPath} ${folder}
    ((total++))
done


counter=1
while [ $counter -lt $total ]; do
	file=Test_$counter/test.csv
    echo "Merging ${file} with ${tests_folder}merged_results.csv..."
    cat $file >> $tests_folder/merged_results.csv
    printf "\n" >> $tests_folder/merged_results.csv
    ((counter++))
done