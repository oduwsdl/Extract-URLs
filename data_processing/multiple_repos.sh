#!/bin/bash
sort -k 3 -k 2n -t ',' -o ./data_processing/pmc_output.csv ./data_processing/pmc_file_url_counts.csv
awk -F',' '{print $1}' ./data_processing/pmc_output.csv |sort|uniq -d|grep -F -f - ./data_processing/pmc_output.csv | sort -k1 -t ',' > ./data_processing/pmc_multiple_repos.csv