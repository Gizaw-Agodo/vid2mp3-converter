from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from app.core.database import get_db

def get_fs_bucket():
    db = get_db()
    if db is  None : 
        raise RuntimeError('http is not initialized')
    fs_bucket = AsyncIOMotorGridFSBucket(db)
    return fs_bucket

async def save_video(file_bytes:bytes, filename:str):
    fs_bucket = get_fs_bucket()
    file_id = await fs_bucket.upload_from_stream(filename, file_bytes)
    return str(file_id)

async def get_video(file_id:str):
    fs_bucket = get_fs_bucket()
    stream = await fs_bucket.open_download_stream(file_id)
    data = await stream.read()
    await stream.close()
    return data