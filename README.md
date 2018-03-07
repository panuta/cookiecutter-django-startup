# Cookiecutter Django Startup

Heavily inspired by [Cookiecutter Django](https://github.com/pydanny/cookiecutter-django), Cookiecutter Django Startup is a boilerplate for small/medium production-ready Django web application project. By including all functions necessary for regular web application (e.g. user registration, development and deployment setup), web application developers doesn't have to do repetitive tasks and focus primarily on what make your web application unique.

## Features
* Django 2.0
* Python 3.6
* User registration via [django-allauth](https://github.com/pennersr/django-allauth)
* Email login / Facebook login (more to come)
* Completed templates for user registration (including email templates)
* Templates uses Bootstrap 4.0 and Font Awesome 5 (can be removed or change to another framework)
* Docker Compose for development and production (using [Gunicorn](http://gunicorn.org/) and [nginx](https://nginx.org/en/) on production)
* HTTPS by default (using [Let's Encrypt](https://letsencrypt.org))
* Integrate with [Mailgun](https://www.mailgun.com/) for sending email (To have much lower chance being marked as SPAM)
 
## User Registration

Currently support login by using email and Facebook account (removable when initialize project)  

Templates for user registration includes

* Login page
* Sign up page
* Email template for signup
* Password recovery page (send recovery email to set a new password)
* Email template for password recovery
* User profile page
* Edit profile page
* Account settings page (change email, change password)
* Email template for changing email (always requires users to verify email)
* Social account settings page (connect/disconnect with social accounts)

Also, django-allauth was customized to serve better user experience on registration
 
* Automatically merge account if users have an existing account that signed up using different methods
* Always requires users logged in from social account to set a password (users will be able to recover their account using password recovery page)
* Automatically logged user in when confirm email

## Initialize project

Install Cookiecutter and run it

    $ pip install cookiecutter
    $ cookiecutter https://github.com/panuta/cookiecutter-django-startup
    
It will ask you a series of question to setup your project. When finished, newly created project will be in your current directory.

To start running your project, I recommend using Docker to easily setup the environment.

First, install [Docker](https://www.docker.com/community-edition) and Docker Compose (if you haven't already). Then go to project directory, build Docker images.

    $ docker-compose -f dev-compose.yml build

If you're using Facebook login, you'll need to fill out Facebook settings before starting Docker containers.

1. Go to [Facebook Apps for Developer](https://developers.facebook.com/apps/) page
2. Open your app dashboard
3. Go to Settings -> Basic
4. Copy App ID and App Secret to `./env/dev.env` file filling out SOCIALACCOUNT_FACEBOOK_CLIENT_ID and SOCIALACCOUNT_FACEBOOK_SECRET variable respectively

Then you can start Docker containers

    $ docker-compose -f dev-compose.yml up

Open `http://127.0.0.1:8000` to see this web application. You can also login to Django admin using `admin` and `admin` as username and password respectively (although it's for development only, you should still change the password to something else)

## Deployment

(Will add more details)

1. Pull code to server
2. Copy content from `./env/prod.env` to production server (do not ever never add this file to git)
2. Build docker images from `prod-compose.yml`
3. Run migration and createsuperuser
4. Start Docker containers using `docker-compose -f prod-compose.yml up -d`
5. Let's Encrypt certificate will be generate automatically in a few minutes
