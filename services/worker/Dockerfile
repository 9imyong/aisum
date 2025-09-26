FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install -U pip && pip install -r requirements.txt
COPY worker_app ./worker_app
CMD ["celery", "-A", "worker_app.celery_app", "worker", "-l", "info", "-Q", "celery"]
