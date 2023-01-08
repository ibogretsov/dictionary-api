FROM python:3.10-alpine

# It is required to install googletrans from source code
RUN apk add git
ENV DICTIONARY_API_MONGODB_URL=

WORKDIR /app/
COPY ./requirements ./requirements

# Install requirements
ARG REQUIREMENTS_FILE
RUN pip install --upgrade pip
RUN pip install -r "requirements/${REQUIREMENTS_FILE:=dev.txt}" && rm -rf requirements

# TODO (ibogretsov): Add app user
COPY app/ ./
ENV PYTHONPATH=/app
