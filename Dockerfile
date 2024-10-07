FROM python:3.12

RUN mkdir /backend_app

WORKDIR /backend_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
