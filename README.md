# smart-ac-backend

[![Build Status](https://travis-ci.org/brad/smart-ac-backend.svg?branch=master)](https://travis-ci.org/brad/smart-ac-backend)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Backend for smart air conditioners. Check out the project's [documentation](http://brad.github.io/smart-ac-backend/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.

Initialize the production server:

```
heroku create smartac-backend-prod --remote prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app smartac-backend-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="smartac-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="smartac.config" \
        DJANGO_EMAIL_HOST="Your smtp host" \
        DJANGO_EMAIL_USE_TLS=True \
        DJANGO_EMAIL_PORT=587 \
        DJANGO_EMAIL_HOST_USER="Your smtp sending email" \
        DJANGO_EMAIL_HOST_PASSWORD="Your smtp account password" \
        --app smartac-backend-prod
```

Initialize the qa server:

```
heroku create smartac-backend-qa --remote qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app smartac-backend-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="smartac-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="smartac.config" \
        DJANGO_EMAIL_HOST="Your smtp host" \
        DJANGO_EMAIL_USE_TLS = True \
        DJANGO_EMAIL_PORT = 587 \
        DJANGO_EMAIL_HOST_USER = "Your smtp sending email" \
        DJANGO_EMAIL_HOST_PASSWORD = "Your smtp account password" \
        --app smartac-backend-qa
```

Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Get your heroku API key from your account settings and use it in this command

```bash
travis encrypt HEROKU_API_KEY="<yourapikey>" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master
```

You're now ready to continuously ship! ✨ 💅 🛳
