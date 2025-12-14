#!/bin/env bash
#arrays are lists in bash
groceries=('milk' 'coffee' 'sugar' 'water')
echo "Showing First Element in The List"
echo "${groceries[0]}"
echo "Showing All Elements in The List"
echo "${groceries[*]}"
echo "Removing third item in the list. Element 2"
unset groceries[2]
echo "${groceries[*]}"
echo "Change a value in the list"
groceries[3]="mango"
echo "${groceries[*]}"


