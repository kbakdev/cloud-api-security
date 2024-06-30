FROM python:3.9-slim

WORKDIR /app

COPY app3/. /app

RUN pip install -r /app/requirements.txt

CMD ["python", "app3.py", "runserver", "0.0.0.0:5000"]
EXPOSE 5000