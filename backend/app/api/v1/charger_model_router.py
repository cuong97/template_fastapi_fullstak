from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from backend.app.common.database import get_db
from backend.app.common.logger import logger
from backend.app.crud.charger_model_crud import charger_model_crud
from backend.app.schemas.charger_model import ChargerModelCreate, ChargerModelResponse
from backend.app.schemas.response import resp
from backend.app.common.handle_error import NotFoundException

charger_model_router = APIRouter()


@charger_model_router.get("s", response_model=List[ChargerModelResponse])
async def list_charger_model(db: Session = Depends(get_db)):
    """
    This endpoint interacts with the list charger-model
    """
    logger.info("endpoint list charger-model")
    results = await charger_model_crud.list(db)
    return resp.success(data=results)


@charger_model_router.post("/create")
async def create_charger(
    charger: ChargerModelCreate, db: Session = Depends(get_db)
) -> dict:
    payload = {**charger.dict()}
    await charger_model_crud.create(db=db, obj_in=payload)
    return payload


@charger_model_router.get("/{id}")
async def get_detail(id: str, db: Session = Depends(get_db)):
    results = await charger_model_crud.get(db, id)
    if not results:
        raise NotFoundException(message="Charger Not Found")
    return resp.success(data=results)
