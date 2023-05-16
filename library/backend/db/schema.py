from pydantic import BaseModel, EmailStr
from datetime import date

class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    last_name: str | None
    email: EmailStr
    password: str
    user_type: str
    book_id_taken: int | None
    reserved_book_id: int | None

    
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


class BookDBModel(BookModel):
    id: int


class BookGetDeleteModel(AuthModel):
    pass

class BookCreateUpdateModel(BookModel, AuthModel):
    pass
