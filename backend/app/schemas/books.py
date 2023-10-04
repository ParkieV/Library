from datetime import UTC, datetime

from pydantic import BaseModel


class BookModel(BaseModel):
	name: str
	authors: str
	book_created_at: datetime | None = datetime.now(tz=UTC)

	class Config:
		orm_mode = True


class BookDBModel(BookModel):
	bookID: int
