import asyncio

from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer

from app import settings
from app.routers import router

app = FastAPI()

app.include_router(router)

consumer: AIOKafkaConsumer


@app.on_event('startup')
async def startup_event():
    global consumer
    global consume_task

    consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPICS,
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
    )

    await consumer.start()

    from app.consumer import consume_messages
    consume_task = asyncio.create_task(
        consume_messages()
    )


@app.on_event('shutdown')
async def shutdown_event():
    await consumer.stop()
    consume_task.cancel()
