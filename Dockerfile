FROM python:3.10-alpine


ENV DICTIONARY_API_MONGODB_URL=

WORKDIR /app/
COPY ./requirements ./requirements

ARG REQUIREMENTS_FILE
RUN pip install --upgrade pip
RUN pip install -r "requirements/${REQUIREMENTS_FILE:=dev.txt}" && rm -rf requirements

COPY app/ ./
