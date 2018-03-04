# Cookiecutter Django Startup

Heavily inspired by [Cookiecutter Django](https://github.com/pydanny/cookiecutter-django) and [Django React Boilerplate](https://github.com/vintasoftware/django-react-boilerplate) project, I stripped its features down and re-created this boilerplate based on my own experiences and preferences.

- Backend: Python 3.6 / Django 2.0
- Frontend: jQuery, Bootstrap 4, Font Awesome 5
- User registration via [django-allauth](https://github.com/pennersr/django-allauth)
- Docker Compose for development and deployment
- Merge email account and social account

## User Account

- Always ask user to set password when sign up using Facebook
- Merge account automatically if user already have existing account created with email

## Usage

- Install cookiecutter
- Run cookiecutter
- Docker compose build
- Docker compose up
- On production, move file .env to production server (without using git)

