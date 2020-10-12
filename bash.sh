#! /bin/bash
cd /home/ubuntu/Blogin
source venv/bin/activate
exec gunicorn -w 4 wsgi:app
