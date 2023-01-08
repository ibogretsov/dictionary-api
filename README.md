# Dictionary API

## Goal

The goal of this API is to provide word definitions/translations taken from Google Translate. *NOTE*: it works only with single words.

## Requirements:
- Python 3.10
- [Docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/) for the development environment

## Run local

- Setup virtual environment. It installs project requirements, linters, tests to virtual environment. Nevertheless it will be better to run tests in container using script (Instructions below in README).
```bash
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip instal -r requirements/dev.txt
```

- Install pre-commit. It allows to check flake8 issues and imports before commit.
```bash
$ pre-commit install
```

- Setup build image
```bash
$ ./scripts/setup.sh
```

- Start (up docker containers). *NOTE* it runs automatically tests. Use flag `-d` to detach containers logs

```bash
$ ./scripts/start.sh -d
```

- Run manually tests. *NOTE* tests will be run it container. It is preffered way.
```bash
$ ./scripts/tests.sh
```

- Stop (stop and delete running containers)

```bash
$ ./scripts/stop.sh
```

### API documentation
When running the development server you may refer to the OpenApi documentation
by visiting http://localhost:8000/docs.
