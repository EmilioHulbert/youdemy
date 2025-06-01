#!/bin/bash
cd /var/
chown -R www-data:www-data  www&
find www -type f -exec chmod 644 {} \;
find www -type d -exec chmod 755 {} \;
chmod 777 /var/www/html/phptutorials/ -R
