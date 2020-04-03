#!/bin/sh
# this script is used to boot a Docker container

openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -subj "/C=US/ST=TN/L=H/O=Cachengo/CN=Cachengo" -keyout key.pem -out cert.pem

flask db upgrade

exec gunicorn -b :5000 --access-logfile - --error-logfile - --certfile cert.pem --keyfile key.pem sso_example:app
