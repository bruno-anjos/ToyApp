#!/usr/bin/env bash

tests_folder=$1
filterResultsPath=$2

rm ${tests_folder}/merged_results.csv

for folder in ${tests_folder}/*/; do
    echo "Filtering results for folder ${folder}"
    ${filterResultsPath} ${folder}
done

for file in ${tests_folder}/*/test.csv; do
    echo "Merging ${file} with ${tests_folder}/merged_results.csv..."
    cat ${file} >> ${tests_folder}/merged_results.csv
    printf "\n" >> ${tests_folder}/merged_results.csv
done