from pydantic import BaseModel, EmailStr
from datetime import date


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: EmailStr | None = None

    class Config:
        orm_mode = True


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
    password: int


class UserDBModel(BaseUserModel):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class AuthModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class BookModel(BaseModel):
    title: str
    authors: str
    user_id_taken: int | None = None
    user_reserved_id: int | None = None
    date_start_use: str | None = None
    date_finish_use: str | None = None

    class Config:
        orm_mode = True


class BookDBModel(BookModel):
    id: int


class BookGetDeleteModel(BaseModel):
    auth: AuthModel | None = None


class BookCreateUpdateModel(BaseModel):
    auth: AuthModel | None = None
    book: BookModel | None = None


class UserGetDeleteModel(BaseModel):
    auth: AuthModel | None = None


class UserCreateUpdateModel(BaseModel):
    auth: AuthModel | None = None
    user: UserModel | None = None


class BookQueryModel(BaseModel):
    user_id: int
    book_id: int
    type_order: str
    type_query: str

    class Config:
        orm_mode = True


class QueryGetDeleteModel(BaseModel):
    auth: AuthModel | None = None


class QueryCreateModel(BaseModel):
    auth: AuthModel | None = None
    query: BookQueryModel | None = None
    