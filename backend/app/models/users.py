from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings import Base


class Users(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(128), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128), unique=True)
    user_type: Mapped[str] = mapped_column(String(10), default="User")
    user_created_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), default=datetime.now(tz=UTC))
