FROM python:3.9-slim

WORKDIR /app

COPY app2/. /app

RUN pip install -r /app/requirements.txt

CMD ["uvicorn", "app2:app", "--host", "0.0.0.0", "--port", "5000"]
EXPOSE 5000
