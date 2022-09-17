#!/bin/bash

#lsof -ti tcp:3300 | xargs kill -9
python3 -m venv RPN_api
source RPN_api/bin/activate
pip3 install -r requirements.txt
uwsgi --socket 0.0.0.0:3300 --protocol=http -w wsgi:app --master  --log-4xx --log-5xx --enable-threads --processes 4 --threads 2

