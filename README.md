# Dictionary API

## Goal

The goal of this API is to provide word definitions/translations taken from Google Translate. *NOTE*: it works only with single words.

## Requirements:
- Python 3.10
- [Docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/) for the development environment

## Run local

- Setup build image
```bash
$ ./scripts/setup.sh
```

- Start (up docker containers). *NOTE* it runs automatically tests. Use flag `-d` to detach containers logs

```bash
$ ./scripts/start.sh -d
```

- Stop (stop and delete running containers)

```bash
$ ./scripts/stop.sh
```

### Runing tests
```bash
$ docker-compose run --rm tests
```

### API documentation
When running the development server you may refer to the OpenApi documentation
by visiting http://localhost:8000/docs.
