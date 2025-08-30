from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.service.mq_service import consume_video_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume_video_message())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("RabbitMQ consumer stopped.")


app = FastAPI(lifespan=lifespan)
