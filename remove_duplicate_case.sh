#!/bin/bash

typeset -l l 

for f in $1/*
do 
  l=$f
  if [ "$l" != "$f" -a -e "$l" ]; then 
    rm "$f"
  elif [ "$l" != "$f" ]; then
    mv $f $l 
  fi
done
