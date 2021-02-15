from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False)
    bolos = Column(Integer, default=0, nullable=False)
    latest_bolo = Column(DateTime, server_default=func.now())
