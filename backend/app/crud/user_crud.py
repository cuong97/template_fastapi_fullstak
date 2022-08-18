from backend.app.crud.base_crud import CRUDBase
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate


class UserCrud(CRUDBase[User, UserCreate, UserCreate]):
    pass


user_crud = UserCrud(User)
