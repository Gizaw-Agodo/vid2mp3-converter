import httpx
from app.core.config import config


async def login_user(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.auth_service_url}/login",
            json={"username": username, "password": password},
        )

        return response.json()
