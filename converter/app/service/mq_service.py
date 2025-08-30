import aio_pika
from aio_pika import Message, DeliveryMode
from app.core.config import config
from aio_pika.abc import AbstractIncomingMessage
import json
import asyncio
from app.service.converter_service import get_video
import tempfile
from app.service.converter_service import convert_to_mp3, save_mp3


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


async def send_audio_message(file_id: str, username: str, filename: str):
    connection = await aio_pika.connect_robust(config.rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(name="audio_queue")
        message_body = {username: username, file_id: file_id, filename: filename}

        message = Message(
            body=json.dumps(message_body).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(message, routing_key="audio_queue")

async def consume_video_message():
    connection = await aio_pika.connect_robust(config.rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(name  = "video_queue", durable=True)
        await queue.consume(process_video_message)
        
        await asyncio.Future()


async def process_video_message(message: AbstractIncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            file_id = body.get('file_id')
            username = body.get('username')
            filename = body.get("filename", f"{file_id}.mp4")


            video_bytes = await get_video(file_id)
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_video:
                tmp_video.write(video_bytes)
                video_path = tmp_video.name

            tmp_file_path =   await convert_to_mp3(video_path)

            with open(tmp_file_path, "rb") as f:
                mp3_bytes = f.read()

            mp3_filename = filename.replace(".mp4", ".mp3")
            mp3_file_id = await save_mp3(mp3_bytes, mp3_filename)

            await send_audio_message(file_id=mp3_file_id, username=username, filename=mp3_filename)

            
            await message.ack()
        except:
            await message.nack()
