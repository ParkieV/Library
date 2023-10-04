from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


class Books(Base):
    __tablename__ = "books"
    bookID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    authors: Mapped[str] = mapped_column(String)
    book_created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now(tz=UTC))
