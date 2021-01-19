#! /bin/bash
cd /home/ubuntu/Blogin
chmod 777 .env
source venv/bin/activate
exec gunicorn -w 4 wsgi:app
