from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..common.database import DBBaseCustom


class Item(DBBaseCustom):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="items")
