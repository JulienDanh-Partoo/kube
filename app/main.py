from contextlib import asynccontextmanager
from typing import Annotated

import pika
from fastapi import Depends, FastAPI
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials))
_global_channel = connection.channel()
_global_channel.queue_declare(queue='test_queue')
_global_channel.exchange_declare(exchange='Business', exchange_type=ExchangeType.fanout)
_global_channel.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    connection.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_channel():
    _channel = connection.channel()
    yield _channel
    _channel.close()


Channel = Annotated[BlockingChannel, Depends(get_channel)]


@app.get("/rabbit")
async def rabbit(channel: Channel):
    message = 'Hello Rabbit'
    channel.basic_publish(exchange='Business', routing_key='Business.edit', body=message)
    return {"message": "Hello Rabbit"}
