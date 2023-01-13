#!/bin/bash
URL=$1
FILE=$2
if [ ! -f "$FILENAME" ]; then
    curl -LI $URL -s > $FILE
    sleep 1
fi
