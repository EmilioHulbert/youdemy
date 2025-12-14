#!/bin/env bash
#If statements
#user="alice"
user=`whoami`

if [ $user = "root" ]
then
  echo "Running the program..."
  date
else
  echo "Please run the script as root"
fi

count=1
if [ $count -lt 1 ]
then
  echo "Wrong input"
else
  echo "Counting"
fi

