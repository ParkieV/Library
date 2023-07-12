from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String,  ForeignKey, DateTime

from app.core.settings import Base 


class Books(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    authors: Mapped[str] = mapped_column(String)
    user_id_taken: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"))
    user_reserved_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"))
    date_start_reserve: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    date_start_use: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    date_finish_use: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
