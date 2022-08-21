from app.common.database import get_db
from app.crud.user_crud import user_crud
from app.models.user import User
from app.schemas.response import resp
from app.schemas.user import UserCreate
from app.services.auth import get_current_user, get_password_hash
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

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


@user_router.post("/")
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


@user_router.get("/get_current_user")
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    This endpoint get authenticated user.
    """
    return resp.success(data=current_user)
