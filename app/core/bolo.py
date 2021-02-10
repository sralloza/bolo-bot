from sqlalchemy.orm.session import Session

from app import crud


def reset_bolos(db: Session):
    users = crud.user.get_multi(db, limit=100000)
    for user in users:
        crud.user.remove(db, id=user.id)
