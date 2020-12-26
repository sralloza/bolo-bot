import logging
from typing import List

from sqlalchemy.orm.session import Session

from app.core.exceptions import AlreadyExistsError
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        if self.get_by_username(db, username=obj_in.username):
            raise AlreadyExistsError(
                f"{obj_in.username!r} ya está registrado, elige otro nombre."
            )

        return super().create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        if obj_in.username is not None:
            if self.get_by_username(db, username=obj_in.username):
                raise AlreadyExistsError(
                    f"{obj_in.username!r} ya está registrado, elige otro nombre."
                )

        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def get_by_username(self, db: Session, *, username: str) -> User:
        return db.query(self.model).filter_by(username=username).first()

    def get_ranking(self, db: Session, *, limit: int = 10) -> List[User]:
        return db.query(self.model).order_by(self.model.bolos.desc()).limit(limit).all()

    def register_bolo(self, db: Session, *, id: int):
        user = self.get_or_404(db, id=id)
        update_user = UserUpdate(bolos=user.bolos + 1)
        return self.update(db, db_obj=user, obj_in=update_user)

    def un_register_bolo(self, db: Session, *, id: int):
        user = self.get_or_404(db, id=id)
        update_user = UserUpdate(bolos=user.bolos - 1)
        return self.update(db, db_obj=user, obj_in=update_user)

    def get_user_position(self, db: Session, *, id: int) -> int:
        user = self.get_or_404(db, id=id)
        return self.get_ranking(db).index(user) + 1


user = CRUDUser(User)
