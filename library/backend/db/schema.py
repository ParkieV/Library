from pydantic import BaseModel
from datetime import datetime
from typing import List

class User(BaseModel):
    name: str
    surname: str
    user_type: str
    email: str
    password: str
    reserved_books: List[int]
    featured_books: List[int]


class Book(BaseModel):
    name: str
    author: str
    src_link: str
    id_reserve: int | None
    start_reserve: datetime
    finish_reserve: datetime