FROM python:3.9-slim

WORKDIR /app
COPY app1/. /app

RUN pip install -r /app/requirements.txt

CMD ["python", "app_flask.py"]
EXPOSE 5000

ENTRYPOINT ["python", "app_flask.py"]