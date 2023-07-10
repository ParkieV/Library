import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String, ForeignKey

from backend.core.db_settings import Base
from backend.models.users import Users
from backend.models.books import Books


class BookQuery(Base):
    __tablename__ = "book_queries"

    id: orm.Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: orm.Mapped[int] = Column(Integer, ForeignKey("users.id"))
    book_id: orm.Mapped[int] = Column(Integer, ForeignKey("books.id"))
    type_order: orm.Mapped[str] = Column(String(10))
    type_query: orm.Mapped[str] = Column(String(10))
