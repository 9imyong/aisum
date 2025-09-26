FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt
COPY run_consumer.py .
CMD ["python", "run_consumer.py"]
