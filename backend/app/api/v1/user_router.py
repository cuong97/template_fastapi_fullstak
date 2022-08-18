from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from backend.app.common.database import get_db
from backend.app.crud.user_crud import user_crud
from backend.app.models.user import User
from backend.app.schemas.response import resp
from backend.app.schemas.user import UserCreate
from backend.app.services.auth import get_current_user, get_password_hash

user_router = APIRouter()


@user_router.get("/")
async def get_users(
    current_user: User = Security(
        get_current_user,
        scopes=["admin", "manager"],
    ),
    db: Session = Depends(get_db),
):
    """
    This endpoint get users
    """
    users = await user_crud.list(db=db)
    return users


@user_router.post("/create")
async def create_user(
    user: UserCreate,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    db: Session = Depends(get_db),
):
    """
    This endpoint interacts with the creation of user
    """
    user.hash_password = get_password_hash(user.hash_password)
    await user_crud.create(db=db, obj_in=user)
    return resp.success(data=user)


@user_router.get("/")
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    This endpoint get authenticated user.
    """
    return resp.success(data=current_user)