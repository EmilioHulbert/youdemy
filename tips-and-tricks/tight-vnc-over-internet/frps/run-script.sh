sudo cp frps /usr/local/bin/
sudo chmod +x /usr/local/bin/frps
sudo mkdir -p /etc/frp
sudo cp frps.toml /etc/frp/
cp frps.service /etc/systemd/system/frps.service
sudo systemctl daemon-reload
sudo systemctl enable --now frps
sudo systemctl status frps
#View live logs: sudo journalctl -u frps -f
#Restart service: sudo systemctl restart frps
