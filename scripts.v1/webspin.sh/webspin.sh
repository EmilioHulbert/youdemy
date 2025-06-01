#!/bin/bash

apt update

apt install php-fpm php-mysql -y

service `ls /etc/init.d |grep php` status
systemctl enable  php8.3-fpm

apt install mysql-client mysql-server -y

apt install nginx -y



