from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


class BookQuery(Base):
    __tablename__ = "book_queries"

    queryID: Mapped[int] = mapped_column(Integer, primary_key=True,
                                        index=True, autoincrement=True)
    userID: Mapped[int] = mapped_column(Integer, ForeignKey(
                                                            "users.userID",
                                                            name="fk__queries_UserID__users"))
    bookID: Mapped[int] = mapped_column(Integer, ForeignKey(
                                                            "books.bookID",
                                                            name="fk__queries_BookID__books"))
    order_type: Mapped[str] = mapped_column(String(10))
    action_type: Mapped[str] = mapped_column(String(10))
