import json

from sqlalchemy import Column, Integer, String, Date, ForeignKey, ARRAY, Null
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    last_name = Column(String, nullable=True, default=Null)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    user_type = Column(String, nullable=False, default="AnonymousUser")
    book_id_taken = Column(Integer, ForeignKey("books.id"), nullable=True, default=Null)
    reserved_book_id = Column(Integer, ForeignKey("books.id"), nullable=True, default=Null)


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    authors = Column(String)
    user_id_taken = Column(Integer, ForeignKey("books.id"), nullable=True, default=Null)
    user_reserved_id = Column(Integer, ForeignKey("books.id"), nullable=True, default=Null)
    date_start_use = Column(Date, nullable=True, default=Null)
    date_finish_use = Column(Date, nullable=True, default=Null)