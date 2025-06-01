#!/bin/bash
pidof openvpn
if [ $? -eq 0 ]; then
echo "Running" >log.log
else
openvpn --config /home/emilio/scripts/remote.config &
fi
