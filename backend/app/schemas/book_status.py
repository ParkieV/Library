from datetime import datetime

from pydantic import BaseModel


class BookStatusModel(BaseModel):
	userID: int
	bookID: int
	type_action: str
	time_start: datetime | None = None
	time_finished: datetime | None = None

class BookStatusDBModel(BookStatusModel):
	id: int
