# Cooking Captchas

Hi, are you also tired of the usual cooking robots? Try our captcha service!

# How to run the service

This repository contains a backend for a microservice written in Python using FastAPI. It stores data in a PostgreSQL database, which is accessed via SQLAlchemy.
This project can be run locally, but it is recommended to launch it in Docker using the `docker compose` command.

## Prerequisites

- Git

- Docker

## Steps

1. Clone the repository

```
git clone https://github.com/SimeoneVilardo/cooking-captchas.git && cd cooking-captchas
```

2. Create the env file

```
cp docker/config/.env.template docker/config/.env
```

3. Run the service

```
docker compose up -d
```

**All done! Now you can test the APIs using cURL or execute commands through Docker.**

# Tests

The recommended way to run the tests is in the Docker container. Once the repo has been cloned and the configuration file added, you can run the tests in Docker with the command:

```
docker compose run --entrypoint "pytest -v --cov=server tests" web
```

Or you can also run mypy:

```
docker compose run --entrypoint "mypy server" web
```

# APIs

The APIs are documented in the OpenAPI format, which you can consult here: [openapi.yaml](./openapi.yaml).

Alternatively, you can get a nice swagger ui interface by running the docker container and going to [localhost:9000/docs](http://localhost:9000/docs) (or locally to [localhost:8000/docs](http://localhost:8000/docs)).

There are two APIs:

- **GET /captcha/** to obtain the captcha image and the captcha id.

- **POST /captcha/** to validate a captcha. You need to pass the guessed value of the captcha image and the captcha id in the body to this endpoint.

## cURL

Receive a captcha in PNG format (the ID will be in the header):

```
curl --location 'http://localhost:9000/captcha/' \
--header 'accept: image/png' \
--output captcha.png -D -
```

Retrieve a captcha in JSON format (the image is in base64):

```
curl --location 'http://localhost:9000/captcha/' \
--header 'accept: application/json'
```

Validate a captcha

```
curl --location 'http://localhost:9000/captcha/' \
--header 'Content-Type: application/json' \
--data '{
"id": 6,
"value": "VAVNE8"
}'
```

# Environment Variables

Regarding environment variables, a template of what is required can be found in the [.env.template](./docker/config/.env.template) file.
To set the environment variables in the devcontainer, simply create a `.env.local` file with the same structure as the template, in the same directory (`docker/config/`). To set the variables used by the `docker compose` command, use the `.env` file.

# Debug

If you want to debug the application, the easiest way is to use a devcontainer with VS Code. For this purpose, there is a `vscode` folder. To set up the devcontainer, simply copy the [devcontainer.json](./vscode/devcontainer.json) and [docker-compose.yml](./vscode/docker-compose.yml) files into your own `.devcontainer` folder. To start the debugger, you can use the [launch.json](./vscode/launch.json) file.
Modify these files according to the specifics of your development environment.

# TODOs

- Manage database migrations (refer: [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html))

- Fix two warnings in pytest

- Don't use consecutive IDs for the captcha. For this proof of concept having the integer was useful, but it should be avoided

- Improve Dockerfile: reduce image size
