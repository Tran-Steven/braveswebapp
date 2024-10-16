FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
