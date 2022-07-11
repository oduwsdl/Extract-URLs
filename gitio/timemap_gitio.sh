#!/bin/bash
while read u; do
    md5ofurl=`echo $u | md5sum | awk '{print $1}'`
    curl -s https://memgator.cs.odu.edu/timemap/json/$u > timemap/$md5ofurl.txt
    sleep 10
    echo $u timemap/$md5ofurl.txt >> test_timemap_map.txt
done < git.io.txt