from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

from app.core.settings import Base


class BookQuery(Base):
    __tablename__ = "book_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    type_order: Mapped[str] = mapped_column(String(10))
    type_query: Mapped[str] = mapped_column(String(10))
