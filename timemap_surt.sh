#!/bin/bash
md5ofurl=`echo $1 | md5sum | awk '{print $1}'`
FILE=timemap/$md5ofurl.txt
if [ -f "$FILE" ]; then
    if [ "$3" != "skip" ]; then
        curl -A "MemGator evogt001@odu.edu" -s http://localhost:1208/timemap/json/$1 > $FILE
        sleep 10
    fi
else 
    curl -A "MemGator evogt001@odu.edu" -s http://localhost:1208/timemap/json/$1 > $FILE
    echo $1 $2 $FILE >> timemap_map.txt
    sleep 3
fi