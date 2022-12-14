from datetime import timedelta

from app.common.database import get_db
from app.common.handle_error import UnAuthorizedException
from app.crud.user_crud import user_crud
from app.schemas.response import resp
from app.schemas.user import Token, UserLogin
from app.services.auth import authenticate_user, create_access_token
from env_settings import env_settings
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    user_data = await user_crud.get(db, data.username)
    user = authenticate_user(user_data, data.password)
    if not user:
        raise UnAuthorizedException(message="Incorrect username or password")
    access_token_expires = timedelta(
        minutes=int(env_settings.access_token_expires_minutes)
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    data = {"access_token": access_token, "token_type": "bearer"}
    return resp.success(data=data)
