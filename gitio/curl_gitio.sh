#!/bin/bash
while read u; do
    md5ofurl=`echo $u | md5sum | awk '{print $1}'`
    curl -LI $u > curl/$md5ofurl.txt
    echo $u curl/$md5ofurl.txt >> curl_map.txt
done < git.io.txt