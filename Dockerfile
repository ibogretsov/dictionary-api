FROM python:3.10-alpine

# It is required to install googletrans from source code
RUN apk add git

ENV DICTIONARY_API_MONGODB_URL= \
    DICTIONARY_API_SOURCE_LANGUAGE=en \
    DICTIONARY_API_TARGET_LANGUAGE=ru

COPY ./requirements ./requirements

# Install requirements
ARG REQUIREMENTS_FILE
RUN pip install --upgrade pip
RUN pip install -r "requirements/${REQUIREMENTS_FILE:=dev.txt}" && rm -rf requirements

# Does not need anymore
RUN apk del git

RUN addgroup -g 1000 -S dictionary && \
    adduser -u 1000 -S dictionary -G dictionary

WORKDIR /app/
COPY app/ ./
USER dictionary
ENV PYTHONPATH=/app
