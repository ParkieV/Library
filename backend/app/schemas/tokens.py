from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: EmailStr | None = None

    class Config:
        orm_mode = True


class BaseAuthToken(Token, TokenData):
    pass


class AuthModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class ButtonData(BaseModel):
    user_id: int
    book_id: int


class BigButtonData(ButtonData):
    email: EmailStr
