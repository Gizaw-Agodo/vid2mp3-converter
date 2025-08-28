from fastapi import FastAPI, UploadFile, Depends
from app.core.database import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from app.services.auth_service import login_user
from app.services.storage_service import save_video
from app.schemas.auth_schema import LoginRequest
from app.core.dependencies import verify_token
from app.services.mq_service import send_video_message
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)


@app.post("/login")
async def login(request: LoginRequest):
    response = login_user(request.username, request.password)
    return response


@app.post("/upload")
async def upload(file: UploadFile, decoded: dict[str, str] = Depends(verify_token)):

    file_bytes = await file.read()
    filename = file.filename or "testfile"

    file_id = await save_video(file_bytes, filename=filename)

    asyncio.create_task(
        send_video_message(file_id, decoded.get("username") or "", filename),
        name=filename,
    )

    return file_id
