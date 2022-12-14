from datetime import datetime, timedelta
from typing import Union

from app.common import handle_error
from app.common.database import get_db
from app.crud.user_crud import user_crud
from env_settings import env_settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{env_settings.api_prefix}/authentication/login"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    this function is used for hashing password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    this function is used for verifying hash password with request password
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def authenticate_user(user, password: str):
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None,
):
    """
    this function is used for creating access token as jwt token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        env_settings.jwt_private_key,
        algorithm=env_settings.jwt_algorithm,
    )
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    This function is used for getting authenticated user.
    """
    try:
        payload = jwt.decode(
            token,
            env_settings.jwt_private_key,
            algorithms=[env_settings.jwt_algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise handle_error.UnAuthorizedException()
    except JWTError:
        raise handle_error.UnAuthenticatedException
    user = await user_crud.get(db, username)
    if not user:
        raise handle_error.UnAuthenticatedException()
    if security_scopes.scopes and (
        not user.role_name or user.role_name not in security_scopes.scopes
    ):
        raise handle_error.UnAuthorizedException(
            message="Not enough permissions",
        )
    return user
