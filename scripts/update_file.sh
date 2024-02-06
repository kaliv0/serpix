#!/usr/bin/env bash

# used for testing tail -f command
val=1
while : 
do
  echo "Hello $val"
  echo "Hello $val" >> dot.txt
  ((val=val+1))
  sleep 1
done
