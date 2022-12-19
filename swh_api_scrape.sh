#!/bin/bash

URL=$1
RESET=$2
REMAINING=$3
TOKEN=$6
if [ ! -f "$4" ]; then
    while [ "$URL" ]; do
        if (( REMAINING == 0 )); then 
            NOW=$(date +%s)
            TIME=$(( RESET - NOW + 1))
            sleep $TIME
        fi

        RESP=$(curl -H "Authorization: Bearer ${TOKEN}" -is "$URL")
        HEADERS=$(echo "$RESP" | sed '/^\r$/q')
        echo $HEADERS >> $4
        CODE=$(echo "$HEADERS" | sed -n -E 's/HTTP\/1.1 ([0-9]+) .*/\1/p')
        LINK=$(echo "$HEADERS" | sed -n -E 's/Link: <(.*)>; rel="next"/\1/p')
        URL=$(echo "$LINK" | tr -d '\r')
        REMAINING=$(echo "$HEADERS" | sed -n -E 's/X-RateLimit-Remaining: ([0-9]+)/\1/p' | tr -d '\r')
        RESET=$(echo "$HEADERS" | sed -n -n -E 's/X-RateLimit-Reset: ([0-9]+)/\1/p' | tr -d '\r')
        PULL=$(echo "$RESP" | sed '1,/^\r$/d')
        echo $PULL >> $5
    done
    echo $CODE $RESET $REMAINING
else
    echo "Repeat"
fi
