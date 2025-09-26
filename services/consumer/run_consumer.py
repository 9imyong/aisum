import os
import asyncio
import json
from aiokafka import AIOKafkaConsumer
from celery import Celery

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "jobs")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("bridge")
celery_app.conf.broker_url = REDIS_URL  # Celery 브로커

async def main():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="job-consumers",
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    print("[consumer] started")
    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode("utf-8"))
            print("[consumer] got:", payload)
            # Celery 태스크로 위임
            celery_app.send_task("worker_app.tasks.process_job", args=[payload])
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(main())
