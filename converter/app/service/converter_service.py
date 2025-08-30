from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from app.core.database import get_mp3_db, get_video_db
from moviepy import VideoFileClip # type: ignore

import asyncio
import tempfile

def get_mp3_bucket():
    db = get_mp3_db()
    if db is  None : 
        raise RuntimeError('db is not initialized')
    fs_bucket = AsyncIOMotorGridFSBucket(db)
    return fs_bucket

def get_video_bucket():
    db = get_video_db()
    if db is None:
        raise RuntimeError('db is nto initialized')
    fs_bucket = AsyncIOMotorGridFSBucket(db)
    return fs_bucket

async def save_mp3(file_bytes:bytes, filename:str):
    fs_bucket = get_mp3_bucket()
    file_id = await fs_bucket.upload_from_stream(filename, file_bytes)
    return str(file_id)

async def get_mp3(file_id:str):
    fs_bucket = get_mp3_bucket()
    stream = await fs_bucket.open_download_stream(file_id)
    data = await stream.read()
    await stream.close()
    return data

async def get_video(file_id:str):
    fs_bucket = get_video_bucket()
    stream = await fs_bucket.open_download_stream(file_id)
    data = await stream.read()
    await stream.close()
    return data

async def convert_to_mp3(video_path: str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _blocking_convert, video_path)

def _blocking_convert(video_path: str):
    clip = VideoFileClip(video_path)
    
    tmp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_file_path = tmp_file.name
    tmp_file.close()
    
    clip.audio.write_audiofile(tmp_file_path)  # type: ignore
    clip.close()
    
    return tmp_file_path
    
