from app.crud.base_crud import CRUDBase
from app.models.charger_model import ChargerModel
from app.schemas.charger_model import ChargerModelCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class ChargerModelCrud(
    CRUDBase[
        ChargerModel,
        ChargerModelCreate,
        ChargerModelCreate,
    ]
):
    async def list_by_owner(
        self,
        db: Session,
        owner: str,
    ) -> list[ChargerModel]:
        return db.query(ChargerModel).filter(ChargerModel.owner == owner).all()


charger_model_crud = ChargerModelCrud(ChargerModel)


class ChargerModelCrudAsync:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[ChargerModel]:
        statement = select(ChargerModel)
        results = await self.session.execute(statement=statement)
        results = results.scalars().all()
        return results

    async def get_first(self) -> list[ChargerModel]:
        statement = select(ChargerModel)
        results = await self.session.execute(statement=statement)
        results = results.scalars().first()
        return results

    async def get(self, id) -> ChargerModel:
        statement = select(ChargerModel).where(ChargerModel.id == id)
        results = await self.session.execute(statement=statement)
        results = results.scalar()
        return results
