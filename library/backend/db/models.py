from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY, Null, Table, 
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    left_id = Column(Integer, ForeignKey('users.id'), primary_key=True),
    right_id = Column(Integer, ForeignKey('books.id'), primary_key=True),
)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    user_type = Column(String, nullable=False, default="AnonymousUser")
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    books = relationship("Books", secondary=association_table, back_populates="books")
    got_books = Column(ARRAY(Integer), ForeignKey('books.id'), nullable=True, default=Null)
    reserved_books = Column(ARRAY(Integer), ForeignKey('books.id'), nullable=True, default=Null)
    favorite_books = Column(ARRAY(Integer), ForeignKey('books.id'), nullable=True, default=Null)


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    src_link = Column(String, nullable=False)
    id_reserve: Column(Integer, ForeignKey("users.id"), nullable=True, default=Null)
    users = relationship("Users", secondary=association_table, back_populates="users")
    reserve_queue = Column(ARRAY(Integer), ForeignKey('users.id'), nullable=True, default=Null)