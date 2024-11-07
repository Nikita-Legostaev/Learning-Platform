from datetime import datetime, timezone
from fastapi import Depends, Request
from jose import jwt

from app.config import Settings
from app.models.users.repositories import UserRepository

settings = Settings()

def get_token(request: Request):
    token = request.cookies.get("Authorization")
    if not token:
        raise Exception("Token not found")
    return token

async def get_current_user(token: str = Depends(get_token)):
    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expair: str = payload.get('exp')
    if int(expair) < int(datetime.now(timezone.utc).timestamp()) and not expair:
        raise Exception("Token expired")
    user = UserRepository.find_by_id(id=int(payload['sub']))
    if not user:
        raise Exception("User not found")
    return user

