from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Any
from app.core.config import config

client: Optional[AsyncIOMotorClient[Any]] = None
mp3_db: Optional[AsyncIOMotorDatabase[Any]] = None
video_db: Optional[AsyncIOMotorDatabase[Any]] = None


async def connect_to_mongo():
    global client, mp3_db, video_db
    client = AsyncIOMotorClient(config.mongodb_url)
    mp3_db = client[config.MONGODB_MP3_DB]
    video_db = client[config.MONGODB_VIDEO_DB]


async def close_mongo_connection():
    global client
    client.close()  # type: ignore


def get_client():
    return client

def get_mp3_db():
    return mp3_db

def get_video_db():
    return video_db