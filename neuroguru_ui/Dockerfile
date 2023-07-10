# Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD streamlit run --server.enableCORS false --browser.serverAddress "0.0.0.0" --server.port $PORT neuroguru.py
