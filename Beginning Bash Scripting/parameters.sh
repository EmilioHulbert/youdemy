#!/bin/env bash
#parameters in bash
#name=$1
#job=$2
#echo "$name works as a $job"
#echo "What is your name? "
#read myname
#echo "You said your name is $myname"
#echo "name of script is $0"
#arrays are lists in bash
groceries=('milk' 'coffee' 'sugar' 'water')
echo "Showing First Element in The List"
echo "${groceries[0]}"
echo "Showing All Elements in The List"
echo "${groceries[*]}"
echo "Removing third item in the list. Element 2"
unset groceries[2]
echo "${groceries[*]}"
echo "Chnage a value in the list"
groceries[3]="mango"
echo "${groceries[*]}"

