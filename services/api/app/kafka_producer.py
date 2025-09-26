import os, asyncio
from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "jobs")

class KafkaProducerSingleton:
    producer: AIOKafkaProducer | None = None

    @classmethod
    async def get(cls):
        if cls.producer is None:
            cls.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
            await cls.producer.start()
        return cls.producer

    @classmethod
    async def close(cls):
        if cls.producer:
            await cls.producer.stop()
            cls.producer = None

async def send_job(payload: dict):
    producer = await KafkaProducerSingleton.get()
    import json
    await producer.send_and_wait(KAFKA_TOPIC, json.dumps(payload).encode("utf-8"))
