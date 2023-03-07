#!/bin/bash
i=1 n=0
while read l; do
    if [ "$n" -gt 0 ]
    then
        IFS=", " read -r -a array <<< $l
        echo ${array[0]}
        u=${array[1]}
        path=${array[3]}
        echo $u
        # filename=`basename `
        # FILE=curl/$md5ofurl.txt
        # if [ ! -f "$FILE" ]; then
        #     curl -LI $u -s > curl/$md5ofurl.txt
        #     echo $u curl/$md5ofurl.txt >> curl_map.txt
        #     sleep 1
        # fi
    fi
    ((n++))
done < test_swh_results.csv

# python3 curl_results.py > swh_curl_results.txt