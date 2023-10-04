from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


class BookStatus(Base):
	__tablename__ = "book_action"

	statusID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
	userID: Mapped[int] = mapped_column(Integer, ForeignKey(
														"users.userID",
														name="fk__book_status__users"))
	bookID: Mapped[int] = mapped_column(Integer, ForeignKey(
														"books.bookID",
														name="fk__book_status__books"))
	type_action: Mapped[str] = mapped_column(String(10))
	time_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
	time_finished: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
