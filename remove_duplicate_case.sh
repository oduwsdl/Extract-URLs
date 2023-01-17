#!/bin/bash

typeset -l l 

for f in $1/*
do 
  l=$f
  if [ "$l" != "$f" -a -e "$l" ]
  then 
    rm "$f"
  fi
done
