from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from jose import jwt
from typing import Any

pwd_context = CryptContext(schemes=['bcrypt'])
def hash_password(password : str):
    return pwd_context.hash(password)

def verify_passowrd (password:str, hash:str):
    return pwd_context.verify(password, hash)

def create_access_token(data : dict[str, Any ]):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(claims = to_encode, key = settings.ACCESS_SECRET_KEY)

def verify_access_token(token : str):
    return jwt.decode(token, key = settings.ACCESS_SECRET_KEY)
    