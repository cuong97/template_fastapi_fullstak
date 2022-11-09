from datetime import datetime

from sqlalchemy.orm import relationship

from app.common.database import DBBaseCustom
from sqlalchemy import Column, DateTime, String, Integer


class User(DBBaseCustom):
    """This is an example model for your application.
    Replace with the *things* you do in your application.
    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String(255), unique=True, index=True)
    hash_password = Column(String(255))
    owner = Column(String(255))
    role_name = Column(String(255))
    email = Column(String(255))
    address = Column(String(255))
    creation = Column(DateTime, default=datetime.utcnow())
    modified = Column(
        DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
    items = relationship("Item", back_populates="user")
