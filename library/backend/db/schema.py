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
    book_id_taken: int
    reserved_book_id: int


class Book(BaseModel):
    id: int
    title: str
    authors: str
    user_id_taken: int
    user_reserved_id: int
    date_start_use: date
    date_finish_use: date