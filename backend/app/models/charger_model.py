from datetime import datetime

from app.common.database import DBBaseCustom
from sqlalchemy import Column, DateTime, String


class ChargerModel(DBBaseCustom):
    __tablename__ = "charger_model"
    id = Column(String(255), unique=True, index=True, primary_key=True)
    name = Column(String(255))
    creation = Column(DateTime, nullable=False, default=datetime.utcnow())
    modified = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
