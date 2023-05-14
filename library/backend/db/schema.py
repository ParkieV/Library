from pydantic import BaseModel, EmailStr
from datetime import date

class User(BaseModel):
    id: int
    name: str
    surname: str
    last_name: str | None
    email: EmailStr
    password: str
    user_type: str
    book_id_taken: int | None
    reserved_book_id: int | None


class Book(BaseModel):
    id: int
    title: str
    authors: str
    user_id_taken: int | None
    user_reserved_id: int | None
    date_start_use: date | None
    date_finish_use: date | None



class ModelAuth(BaseModel):
    email: EmailStr
    password: str

class BookGetDelete(ModelAuth):
    pass

class BookUpdate(ModelAuth, Book):
    pass