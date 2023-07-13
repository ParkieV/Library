from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime

from app.core.settings import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(128), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128), unique=True)
    user_type: Mapped[str] = mapped_column(String(10), default="AnonymousUser")
    book_id_taken: Mapped[int | None] = mapped_column(Integer, ForeignKey("books.id"))
    reserved_book_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("books.id"))
    access_token: Mapped[str | None] = mapped_column(String(128), default=None)
    time_token_create: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), default=None)
