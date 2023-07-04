import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy import types

from typing import Optional

from backend.core.db_settings import Base 


class Books(Base):
    __tablename__ = "books"
    id: orm.Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: orm.Mapped[str] = Column(String)
    authors: orm.Mapped[str] = Column(String)
    user_id_taken: orm.Mapped[Optional[int]] = Column(Integer, ForeignKey("users.id"))
    user_reserved_id: orm.Mapped[Optional[int]] = Column(Integer, ForeignKey("users.id"))
    date_start_reserve: orm.Mapped[Optional[types.DateTime]] = Column(DateTime(timezone=True))
    date_start_use: orm.Mapped[Optional[types.DateTime]] = Column(DateTime(timezone=True))
    date_finish_use: orm.Mapped[Optional[types.DateTime]] = Column(DateTime(timezone=True))
