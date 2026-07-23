#!/usr/bin/env bash
set -o errexit
cd /opt/render/project/src
pip install -r requirements.txt
python manage.py collectstatic --noinput
