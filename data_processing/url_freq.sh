#!/bin/bash
sort -k3 -k2n -t ',' ./data_processing/pmc_file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | sort | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > ./data_processing/pmc_URL_frequency.csv
sort -k3 -k2n -t ',' ./data_processing/file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | sort | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > ./data_processing/URL_frequency.csv
sort -k3 -k2n -t ',' ./data_processing/class_file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | sort | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > ./data_processing/class_URL_frequency.csv
sort -k3 -k2n -t ',' ./data_processing/tamu_file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | sort | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > ./data_processing/tamu_URL_frequency.csv
sort -k3 -k2n -t ',' ./data_processing/etd_file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | sort | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > ./data_processing/etd_URL_frequency.csv
