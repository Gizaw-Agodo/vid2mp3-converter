from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Any
from app.core.config import config

client: Optional[AsyncIOMotorClient[Any]] = None
db: Optional[AsyncIOMotorDatabase[Any]] = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(config.mongodb_url)
    db = client[config.MONGODB_DB]


async def close_mongo_connection():
    global client
    client.close()  # type: ignore


def get_client():
    return client

def get_db():
    return db
