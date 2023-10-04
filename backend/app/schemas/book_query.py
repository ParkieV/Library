from pydantic import BaseModel, EmailStr


class BookQueryModel(BaseModel):
	userID: int
	bookID: int
	order_type: str
	action_type: str


class BookQueryDBModel(BookQueryModel):
	queryID: int

	class Config:
		orm_mode = True

class QueryActionModel(BaseModel):
	userID: int
	bookID: int

class UserQueryActionModel(QueryActionModel):
	email: EmailStr
