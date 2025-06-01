#!/bin/env bash
#*-*-Creator:EmilioHulbert
#*-*-Date:6/4/2025

#Color definitions
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
#EndColor definitions
echo -e "$red_f Starting Script. $reset_f"
echo

echo -e "$magenta_f Removing current symbolic links :) $reset_f"
#Remac error link file search when using switch -name ".sh" in links pointing to files
find /opt/scripts/ -maxdepth 1  -type l -exec rm -f {} \;
echo -e "$yellow_f Creating New symbolic links :) $reset_f"
find /opt/scripts/ -mindepth 2 -maxdepth 2 -type f -name "*.sh" | while read -r script ;do   link_name="/opt/scripts/$(basename "$script" .sh)" ; ln -s "$script" "$link_name";done

echo -e "$green_f Done !"
exit 0

