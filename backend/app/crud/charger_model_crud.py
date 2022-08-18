from sqlalchemy.orm import Session

from backend.app.crud.base_crud import CRUDBase
from backend.app.models.charger_model import ChargerModel
from backend.app.schemas.charger_model import ChargerModelCreate


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
