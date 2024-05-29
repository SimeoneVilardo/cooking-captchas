# Cooking Captchas

Hi, are you also tired of the usual cooking robots? Try our captcha service!


# How to run the service

This repository contains a backend for a microservice written in Python using FastAPI. You can run the backend using Docker. There is also a PostgreSQL database, which is accessed via SQLAlchemy.
## Prerequisites
* git
* docker

## Steps
1) Clone the repository
```
git clone https://github.com/SimeoneVilardo/cooking-captchas.git && cd cooking-captchas
```
2) Create the env file (you can start with the template)
```
cp docker/config/.env.template docker/config/.env
```
2) Run the service
```
docker compose up
```

# Tests
The recommended way to run the tests is in the Docker container. Once the repo has been cloned and the configuration file added, you can run the tests in Docker with the command:
```
docker compose run --entrypoint "pytest test" web
```
Or you can also run mypy:
```
docker compose run --entrypoint "mypy ." web
```

# APIs
The APIs are documented in the OpenAPI format, which you can consult here: [openapi.yaml](./openapi.yaml).
Alternatively, you can also run the microservice (even with Docker Compose!) and go to [http://localhost:9000/docs](http://localhost:9000/docs).
Ci sono due API:
-   **GET /captcha/** to obtain the captcha image and the captcha id.
-   **POST /captcha/** to validate a captcha. You need to pass the guessed value of the captcha image and the captcha id in the body to this endpoint.

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