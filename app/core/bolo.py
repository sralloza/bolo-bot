from sqlalchemy.orm.session import Session

from app import crud
from app.schemas.user import UserUpdate


def reset_bolos(db: Session):
    users = crud.user.get_multi(db, limit=1000)
    for user in users:
        obj_in = UserUpdate(bolos=0)
        crud.user.update(db, db_obj=user, obj_in=obj_in)
