from pydantic import BaseModel, EmailStr


class BaseUserModel(BaseModel):
	name: str
	surname: str
	last_name: str | None = None
	email: EmailStr
	user_type: str = "User"
	book_id_taken: int | None = None
	reserved_book_id: int | None = None
	access_token: str | None = None
	time_token_create: str | None = None


class UserModel(BaseUserModel):
	password: str


class UserHashedModel(BaseUserModel):
	hashed_password: str

	class Config:
		orm_mode = True


class UserDBModel(UserHashedModel):
	id: int

	class Config:
		orm_mode = True

class loginData(BaseModel):
	email: EmailStr
	password: str
