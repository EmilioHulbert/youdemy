[Unit]
Description=Nashtech Solutions Django Application
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/remacode.com
Environment=DJANGO_KEY='%vr*f84xkd)t&)#ep@83t-wpyl!^%cv-9z33!g982^64d-!q8'
Environment=DJANGO_ALLOW_ASYNC_UNSAFE=true

ExecStart=/var/www/remacode.com/venv/bin/python manage.py runserver 0.0.0.0:8002
Restart=always

[Install]
WantedBy=multi-user.target


