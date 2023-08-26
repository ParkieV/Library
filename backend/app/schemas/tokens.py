from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenPayload(BaseModel):
	sub: EmailStr = Field(default=None, description="Почта")
	exp: datetime | float = Field(default=None, description="Дата истечения токена")

class RefreshTokenModel(BaseModel):
	refresh_token: str

class TokensModel(RefreshTokenModel):
	access_token: str


