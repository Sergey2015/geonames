FROM python:3.11

WORKDIR  /app

RUN pip install --upgrade pip

COPY  app/main.py app/main.py
COPY  app/templates app/templates/
COPY  app/static app/static/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8007

COPY app/pack app/pack
COPY app/data app/data
COPY app/config.env app/config.env
COPY app/static app/static
COPY app/templates app/templates

RUN apt-get update && apt-get install -y nano

CMD cd app && uvicorn main:app --host 0.0.0.0 --port 8007