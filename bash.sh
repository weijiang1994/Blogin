#! /bin/bash
cd /home/ubuntu/Blogin
chmod 777 .env
source venv/bin/activate
exec gunicorn -c gunicorn_conf.py wsgi:app