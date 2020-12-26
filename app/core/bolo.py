from app import crud
from app.db.session import get_db
from app.schemas.user import UserUpdate


def reset_bolos():
    with get_db() as db:
        users = crud.user.get_multi(db, limit=1000)
        for user in users:
            obj_in = UserUpdate(bolos=0)
            crud.user.update(db, db_obj=user, obj_in=obj_in)
