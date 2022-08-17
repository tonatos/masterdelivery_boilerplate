from fastapi import FastAPI
from mm_kafka.messaging.base import KafkaProducer
from ..settings import settings


async def connect_to_kafka(app: FastAPI) -> None:
    if settings.kafka.KAFKA_BROKERS:
        producer: KafkaProducer = KafkaProducer(
            name=settings.kafka.KAFKA_PRODUCE_TOPIC,
            bootstrap_servers=settings.kafka.KAFKA_BROKERS
        )
        await producer.init()
        app.state.producer = producer


async def close_kafka_connection(app: FastAPI) -> None:
    if settings.kafka.KAFKA_BROKERS:
        await app.state.producer.close()
