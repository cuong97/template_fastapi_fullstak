from typing import List

from app.common.database import get_async_session, get_db
from app.common.handle_error import NotFoundException
from app.common.logger import logger
from app.crud.charger_model_crud import ChargerModelCrudAsync as charger_async
from app.crud.charger_model_crud import charger_model_crud
from app.schemas.charger_model import ChargerModelCreate, ChargerModelResponse
from app.schemas.response import resp
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

charger_model_router = APIRouter()


@charger_model_router.get("s", response_model=List[ChargerModelResponse])
async def list_charger_model(
    db_async: AsyncSession = Depends(get_async_session),
    db: Session = Depends(get_db),
):
    """
    This endpoint interacts with the list charger-model
    """
    logger.info("endpoint list charger-model")
    results = await charger_model_crud.list(db)
    await charger_async(session=db_async).get_first()
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
