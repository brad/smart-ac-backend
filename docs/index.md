# smart-ac-backend

[![Build Status](https://travis-ci.org/brad/smart-ac-backend.svg?branch=master)](https://travis-ci.org/brad/smart-ac-backend)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Backend for smart air conditioners. Check out the project's [documentation](http://brad.github.io/smart-ac-backend/). Developers, see below, administrators check the documentation [here](admin/index.md).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```


# Continuous Deployment

Deployment automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Enable this by:

Creating the production sever:

```
heroku create smartac-prod --remote prod && \
    heroku addons:create newrelic:wayne --app smartac-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app smartac-prod && \
    heroku config:set DJANGO_SECRET=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="smartac-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="smartac.config" \
        DJANGO_EMAIL_HOST="Your smtp host" \
        DJANGO_EMAIL_HOST_USER="Your smtp sending email" \
        DJANGO_EMAIL_HOST_PASSWORD="Your smtp account password" \
        --app smartac-prod
```

Creating the qa sever:

```
heroku create `smartac-qa --remote qa && \
    heroku addons:create heroku-postgresql:hobby-dev && \
    heroku config:set DJANGO_SECRET=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="smartac-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="smartac.config" \
        DJANGO_EMAIL_HOST="Your smtp host" \
        DJANGO_EMAIL_HOST_USER="Your smtp sending email" \
        DJANGO_EMAIL_HOST_PASSWORD="Your smtp account password" \
        --app smartac-qa
```

Securely add your heroku credentials to travis so it can automatically deploy your changes.

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Get your heroku API key from your account settings and use it in this command

```bash
travis encrypt HEROKU_API_KEY="<yourapikey>" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -m "ci(travis): added heroku credentials" && \
git push origin master && \
git checkout -b qa && \
git push -u origin qa
```
You're ready to continuously ship! ✨ 💅 🛳
