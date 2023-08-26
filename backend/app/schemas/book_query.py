from pydantic import BaseModel, EmailStr


class BookQueryModel(BaseModel):
	user_id: int
	book_id: int
	type_order: str
	type_query: str


class BookQueryDBModel(BookQueryModel):
	id: int

	class Config:
		orm_mode = True

class QueryActionModel(BaseModel):
	user_id: int
	book_id: int

class UserQueryActionModel(QueryActionModel):
	email: EmailStr
