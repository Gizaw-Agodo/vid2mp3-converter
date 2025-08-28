import aio_pika
from aio_pika import Message, DeliveryMode
from app.core.config import config
import json


async def send_video_message(file_id: str, username: str, filename: str):
    connection = await aio_pika.connect_robust(config.rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(name="video_queue")
        message_body = {username: username, file_id: file_id, filename: filename}

        message = Message(
            body=json.dumps(message_body).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(message, routing_key="video_queue")
