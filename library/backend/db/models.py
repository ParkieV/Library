import json

from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)
    user_type = Column(String, nullable=False, default="AnonymousUser")
    book_id_taken = Column(Integer, ForeignKey("books.id"), nullable=True)
    reserved_book_id = Column(Integer, ForeignKey("books.id"), nullable=True)
    access_token = Column(String, nullable=True, default=None)
    time_token_create = Column(DateTime(timezone=True), nullable=True, default=None)


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    authors = Column(String)
    user_id_taken = Column(Integer, ForeignKey("books.id"), nullable=True)
    user_reserved_id = Column(Integer, ForeignKey("books.id"), nullable=True)
    date_start_reserve = Column(DateTime(timezone=True), nullable=True)
    date_start_use = Column(DateTime(timezone=True), nullable=True)
    date_finish_use = Column(DateTime(timezone=True), nullable=True)

class BookQuery(Base):
    __tablename__ = "book_queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    type_order = Column(String, nullable=False)
    type_query = Column(String, nullable=False)
