from sqlalchemy.orm.session import Session

from app import crud
from app.schemas.user import UserUpdate


def reset_bolos(db: Session):
    users = crud.user.get_multi(db, limit=1000)
    for user in users:
        crud.user.remove(db, id=user.id)
