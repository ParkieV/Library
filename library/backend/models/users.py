import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy import types

from typing import Optional

from backend.core.db_settings import Base
from backend.models.books import Books


class Users(Base):
    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(String(50))
    surname: orm.Mapped[str] = orm.mapped_column(String(50))
    last_name: orm.Mapped[Optional[str]] = orm.mapped_column(String(50), )
    email: orm.Mapped[str] = orm.mapped_column(String(128), unique=True)
    hashed_password: orm.Mapped[str] = orm.mapped_column(String(128), unique=True)
    user_type: orm.Mapped[str] = orm.mapped_column(String(10), default="AnonymousUser")
    book_id_taken: orm.Mapped[Optional[int]] = orm.mapped_column(Integer, ForeignKey("books.id"))
    reserved_book_id: orm.Mapped[Optional[int]] = orm.mapped_column(Integer, ForeignKey("books.id"))
    access_token: orm.Mapped[Optional[str]] = orm.mapped_column(String(128), default=None)
    time_token_create: orm.Mapped[Optional[types.DateTime]] = Column(DateTime(timezone=True), default=None)
