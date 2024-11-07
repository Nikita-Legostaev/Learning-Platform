from fastapi import APIRouter, Depends, Response

from app.auth.auth import authenticate_user, create_access_token, get_password_hash
from app.auth.dependes import get_current_user
from app.models.users.model import User
from app.models.users.repositories import UserRepository
from app.auth.shemas import SUserAuth, SUserRegister


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register')
async def register(user_data: SUserRegister):
    existing_user = await UserRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        raise Exception('email found')
    hasshed_password = get_password_hash(user_data.password)
    await UserRepository.add(email=user_data.email, password_hash=hasshed_password, username=user_data.username)
    return {'message': 'User registered'}

@router.post('/login')
async def login(user_data: SUserAuth, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise Exception('Invalid credentials')
    acces_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='Authorization', value=acces_token)
    return {'access_token': acces_token, 'token_type': 'bearer'}

@router.post('/logout')
async def logout(responce: Response, current_user: User = Depends(get_current_user)):
    responce.delete_cookie(key='Authorization')
    return {'message': 'Logged out'}



