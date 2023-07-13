from sqlalchemy import text, select
from fastapi import status

from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.books import Books

from app.schemas.books import BookDBModel, BookModel


async def search_book_by_title(session: AsyncSession, book_title: str) -> BookDBModel:
    query = text("""
                     SELECT *
                     FROM books
                     WHERE title LIKE :new_title
                     LIMIT 10;
                """)

    result = await session.execute(query, {"new_title": "%" + book_title + "%"})

    result = result.all()
    books = [BookDBModel.from_orm(row) for row in result]
    return books


async def create_book(session: AsyncSession, book_schema: BookModel) -> BookModel:
    book_model = Books(**book_schema.dict())

    session.add(book_model)

    await session.commit()
    return BookModel.from_orm(book_schema)


async def get_book_by_id(session: AsyncSession, book_id: int) -> BookDBModel:
    query = text("""
            SELECT *
            FROM books
            WHERE id = :id;
        """)

    result = await session.execute(query, {"id": book_id})

    if not (result := result.one_or_none()):    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book = result
    await session.commit()
    return BookDBModel.from_orm(book)


async def delete_book_by_id(session: AsyncSession, book_id: int) -> BookDBModel:
    query = text("""
                     DELETE FROM books
                     WHERE id = :id
                     RETURNING *;
                """)

    result = await session.execute(query, {"id": book_id})

    if not (result := result.one_or_none()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book = result
    await session.commit()
    return BookDBModel.from_orm(book)


async def update_book(session: AsyncSession, book_schema: BookDBModel) -> BookDBModel:
    query = text("""
                         UPDATE books
                         SET (name, authors, user_id_taken, user_reserved_id, date_start_reserve, date_start_use, date_finish_use) = 
                         (:name, :authors, :user_id_taken, :user_reserved_id, :date_start_reserve, :date_start_use, :date_finish_use) 
                         WHERE id = :id
                         RETURNING *;
            """)

    result = await session.execute(query, book_schema.dict())

    if not (result := result.one_or_none()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book = result
    await session.commit()
    return BookDBModel.from_orm(book)


async def get_books(session: AsyncSession, offset_db: int | None = None, limit_db: int | None = None) -> BookDBModel:
    result = session.execute(
        select(Books).offset(offset_db).limit(limit_db))
    result = result.all()
    users = [BookDBModel.from_orm(row) for row in result]
    return users
