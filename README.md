# Dictionary API

## Goal

The goal of this API is to provide word definitions/translations taken from Google Translate. *NOTE*: it works only with single words.

## Requirements:
- Python 3.10
- [Docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/) for the development environment

## Run project locally on your computer

### Project is fully dockerized. So to start it you just need few commands.

- Build docker images
```bash
docker compose build --no-cache
```

- Start (up docker containers). *NOTE* In docker-compose file there is a service for tests. So when you start docker compose up it will runs automatically tests (container dictionary-api-tests-1).

```bash
docker compose up -d
```

- You can run tests manually.
```bash
docker start -a dictionary-api-tests-1
```

- Stop (stop and delete running containers)

```bash
docker compose down
```

## Development

For development you need to have Python 3.10. If you already know how to setup python virtual environemnt and set up it for your favourite IDE/redactor you can skip this part. You can manage your python interpretators using pyenv.

- Install [pyenv](https://github.com/pyenv/pyenv#installation). Follow all instructions.

- Install Python 3.10 using pyenv. It can take few minutes.
```bash
pyenv install 3.10.9
```

- Choose 3.10 as shell-specific Python version
```bash
pyenv shell 3.10.9
```

- Create virtual environment and activate it
```bash
pyenv virtualenv dictionary-api && pyenv activate dictionary-api
```

- Install dev requirements
```bash
pip install -r requirements/dev.txt
```

- Install pre-commit. It allows to check flake8 issues and imports before commit.
```bash
pre-commit install
```

- Check that pre-commit works fine
```bash
pre-commit run --all-files
```

## API documentation
When running the development server you may refer to the Swagger documentation by visiting http://localhost:8000/docs.

## Assumptions and Constraints

It is not an ideal solution. There are few assumptions and constraints which need to be kept in mind.
- 1: To translate words and get info this app uses logic the same as for [translate page](https://translate.google.com/?sl=en&tl=ru&text=challenge&op=translate)). It is not a great solution because it requires additional libraries to parse response which is supposed for browsers. If you send too many requests (1 in one second for example your API can be banned).
Google Cloud provides [special translation service](https://cloud.google.com/translate/docs/reference/rest/).
- 2: From point 1. In the project is used [pygoogletrans](https://github.com/ssut/py-googletrans) to send a request which translation page send to the API and process response. Project is not very stable, so it was needed to fork it and update dependencies and code (this library was using the old httpx version, so there were conflicts between this library and fastapi dependencies).
- 3: Currently it is used to for en -> ru translations.
- 4: It will be better to migrate from requirements and pip to the [Poetry](https://python-poetry.org/) and toml configs.
