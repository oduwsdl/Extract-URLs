#!/bin/bash
sort -k3 -k2n -t ',' file_url_counts.csv | sed 's/,/ /g' | cut -f2,3 -d ' ' | uniq -c | sed -e 's/^[[:space:]]*//' | sed -e "s/ /,/g" > URL_frequency.csv