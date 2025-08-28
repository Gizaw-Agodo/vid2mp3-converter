from fastapi import Header, HTTPException
import httpx
from app.core.config import config


async def verify_token(authrization: str = Header(...)):
    if not authrization.startswith("Bearer"):
        raise HTTPException(detail="No authroization header", status_code=401)

    token = authrization.split(" ")[1]
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.auth_service_url}/verify", json={"token": token}, timeout=5
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
