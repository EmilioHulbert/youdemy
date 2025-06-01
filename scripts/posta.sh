#!/bin/env bash

#Author :- Remac
#Created :- 01-6-2025
#Description :- Curl upload file automator


declare  reset_f="\033[0m"
declare  green_f="\033[32m"
declare black_f="\033[30m"
declare yellow_f="\033[33m"
declare magenta_f="\033[35m"
declare white_f="\033[37m"
declare  dim="\033[2m"
declare italic="\033[3m"
declare  underline="\033[4m"
declare red_f="\033[31m"
declare reset="\033[0m"

if [[ ! "${1}" ]];then
	printf "This script Must Take A File Argument\n"
	exit 1
elif [[ "${#}" -gt 1 ]]; then
		#statements
		printf "This script Can Only Post One File At A Time\n"
		exit 1
else
	#Check if file exist
	if [[ -f "${1}" ]]; then
		#statements
		echo -e "Uploading File $yellow_f${1}$reset"
	else
		printf "${red_f}File ${1} does not exist in the specified directory $reset \n"
		exit 1
	fi
	#Proceed to upload File
	curl --upload-file "{$1}" https://nairobiskates.com/uploads/
	echo -e "${green_f}Done !${reset_f}"
fi
exit 0
