# smart-ac-backend

[![Build Status](https://travis-ci.org/brad/smart-ac-backend.svg?branch=master)](https://travis-ci.org/brad/smart-ac-backend)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Backend for smart air conditioners. Check out the project's [documentation](http://brad.github.io/smart-ac-backend/).

# Future Development

Unfortunately, I ran out of time to complete all the requirements on this project. If I had just a bit more time I would do the following:

- Adjust the template for the device page in the admin in the following ways:
  - Enable the filtering of sensor logs by "this week", "this month", or "this year"
  - Plug in real data to the sensor log chart
  - Display sensor logs and health data in an orderable table format
- Only allow admins to send invitations as themselves
- Set up a system to notify logged in admins when there is an alerting device and a way for them to resolve these notifications
- Write a fake smartac client to generate real time data for testing

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
