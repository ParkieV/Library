from pydantic import BaseModel, EmailStr
from datetime import date

class UserModel(BaseModel):
    name: str
    surname: str
    last_name: str | None = None
    email: EmailStr
    password: str
    user_type: str = "AnonymousUser"
    book_id_taken: int | None = None
    reserved_book_id: int | None = None

class UserDBModel(UserModel):
    id: int

    
class AuthModel(BaseModel):
    email: EmailStr
    password: str


class BookModel(BaseModel):
    title: str
    authors: str
    user_id_taken: int | None = None
    user_reserved_id: int | None = None
    date_start_use: date | None = None
    date_finish_use: date | None = None

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