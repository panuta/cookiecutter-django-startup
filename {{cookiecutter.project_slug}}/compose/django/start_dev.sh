#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
{% if cookiecutter.auto_create_super_user == 'y' -%}python manage.py auto_createsuperuser
{% endif %}{% if cookiecutter.login_by_social_accounts == 'y' -%}python manage.py auto_createsocialapp
{% endif %}python manage.py runserver 0.0.0.0:8000
