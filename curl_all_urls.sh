#!/bin/bash
i=1 n=0
while read l; do
    if [ "$n" -gt 0 ]
    then
        IFS=' ' read -r -a array <<< $l
        u=${array[0]}
        md5ofurl=`echo $u | md5sum | awk '{print $1}'`
        curl -LI $u > curl/$md5ofurl.txt
        echo $u curl/$md5ofurl.txt >> curl_map.txt
    fi
    ((n++))
done < timemap_results.csv

python3 curl_results.py > curl_results.txt