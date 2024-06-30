FROM python:3.9-slim

WORKDIR /app

COPY app5/. /app

RUN pip install -r /app/requirements.txt

CMD ["python", "app_tornado.py"]
EXPOSE 5000
