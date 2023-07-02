import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String,  ForeignKey


Base = orm.declarative_base()

class BookQuery(Base):
    __tablename__ = "book_queries"

    id: orm.Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True, init=False, sort_order=-9999, use_existing_column=False)
    user_id: orm.Mapped[int] = Column(Integer, ForeignKey("users.id"))
    book_id: orm.Mapped[int] = Column(Integer, ForeignKey("books.id"))
    type_order: orm.Mapped[str] = Column(String(10))
    type_query: orm.Mapped[str] = Column(String(10))
