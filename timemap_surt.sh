#!/bin/bash
URL=$1
FILE=$2
if [ -f "$FILE" ]; then
    if [ "$3" != "skip" ]; then
        curl -A "MemGator evogt001@odu.edu" -s https://memgator.cs.odu.edu/timemap/json/$URL > $FILE
        sleep 3
    fi
else 
    curl -A "MemGator evogt001@odu.edu" -s https://memgator.cs.odu.edu/timemap/json/$URL > $FILE
    sleep 3
fi