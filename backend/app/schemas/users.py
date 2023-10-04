from datetime import UTC, datetime

from pydantic import BaseModel, EmailStr


class BaseUserModel(BaseModel):
	first_name: str
	surname: str
	last_name: str | None = None
	email: EmailStr
	user_type: str = "User"
	user_created_at: datetime | None = datetime.now(tz=UTC)


class UserModel(BaseUserModel):
	password: str


class UserHashedModel(BaseUserModel):
	hashed_password: str

	class Config:
		orm_mode = True


class UserDBModel(UserHashedModel):
	userID: int

	class Config:
		orm_mode = True

class loginData(BaseModel):
	email: EmailStr
	password: str
