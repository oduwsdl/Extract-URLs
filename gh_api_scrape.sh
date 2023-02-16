#!/bin/bash

URL=$1
RESET=$2
REMAINING=$3
TOKEN=$6
if [ ! -f "$5" ]; then
    if (( REMAINING == 0 )); then
        NOW=$(date +%s)
        TIME=$(( RESET - NOW + 1 ))
        sleep $TIME
    fi

    RESP=$(curl -L -H "Authorization: Bearer ${TOKEN}" -H "X-GitHub-Api-Version: 2022-11-28" -H "Accept: application/vnd.github+json" -is "$URL")
    # RESP=$(curl -H "X-GitHub-Api-Version: 2022-11-28" -H "Accept: application/vnd.github+json" -is "$URL")
    HEADERS=$(echo "$RESP" | sed '/^\r$/q')
    echo $RESP >> $4
    REMAINING=$(echo "$HEADERS" | sed -n -E 's/x-ratelimit-remaining: ([0-9]+)/\1/p' | tr -d '\r')
    RESET=$(echo "$HEADERS" | sed -n -n -E 's/x-ratelimit-reset: ([0-9]+)/\1/p' | tr -d '\r')
    PULL=$(echo "$RESP" | sed -n '/^$/{g;D;}; N; $p;')
    echo $PULL >> $5
    echo $RESET $REMAINING
else
    echo "Repeat"
fi