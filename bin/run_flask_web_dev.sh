#!/bin/sh

export PYTHONPATH=".:/var/www/html/Pingback"
export REDIS_HOST=""
export REDIS_PORT=
export REDIS_PASSWORD=""
export REDIS_DB=0
export FLASK_APP="/var/www/html/Pingback/flask_web/main.py"

/var/www/html/py3_env/bin/flask run -h 0.0.0.0 -p 80
