FROM python:3.9-slim

WORKDIR /app

COPY app4/. /app

RUN pip install -r /app/requirements.txt

CMD ["python", "app_bottle.py"]
EXPOSE 5000
