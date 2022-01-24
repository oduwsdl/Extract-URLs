#!/bin/bash
sort -k 3 -k 2n -t ',' -o output.csv file_url_counts.csv
awk -F',' '{print $1}' output.csv |sort|uniq -d|grep -F -f - output.csv | sort -k1 -t ',' multiple_repos.csv