from datetime import datetime, timezone, timedelta
from fastapi import Depends, Request
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from fastapi.exceptions import HTTPException

from app.config import Settings
from app.models.users.repositories import UserRepository

settings = Settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encode_jwt

async def authenticate_user(email: str, password: str) -> dict:
    user = await UserRepository.find_one_or_none(email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    await UserRepository.update_last_login(user.id)
    return user
