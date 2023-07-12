from sqlalchemy import text, select
from fastapi import status

from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.books import Books

from app.schemas.books import BookDBModel, BookModel
from app.schemas.error import ErrorModel


class BookMethods():

    async def search_book_by_title(session: AsyncSession, book_title: str) -> BookDBModel | ErrorModel:
        query = text("""
                     SELECT *
                     FROM books
                     WHERE title LIKE :new_title
                     LIMIT 10;
                """)
        try:
            result = await session.execute(query, {"new_title": "%" + book_title + "%"})
            
            result = result.all()
            books = [BookDBModel.from_orm(row) for row in result]
            return books
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def create_book(session: AsyncSession, book_schema: BookModel) -> BookModel | ErrorModel:
        try:
            book_model = Books(**book_schema.dict())
            
            session.add(book_model)

            await session.commit()
            return BookModel.from_orm(book_schema)
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def get_book_by_id(session: AsyncSession, book_id: int) -> BookDBModel | ErrorModel:
        query = text("""
            SELECT *
            FROM books
            WHERE id = :id;
        """)

        try:
            result = await session.execute(query, {"id": book_id})

            if not (result := result.one_or_none()):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            
            result = result.one_or_none()
            book = result
            await session.commit()
            return BookDBModel.from_orm(book)
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def delete_book_by_id(session: AsyncSession, book_id: int) -> BookDBModel | ErrorModel:
        query = text("""
                     DELETE FROM books
                     WHERE id = :id
                     RETURNING *;
                """)
        try:
            result = await session.execute(query, {"id": book_id})
            result = result.one_or_none()
            if result:
                book = result
                await session.commit()
                return BookDBModel.from_orm(book)
            else:
                raise ValueError("Book not found.")
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def update_book(session: AsyncSession, book_schema: BookDBModel) -> BookDBModel | ErrorModel:
        try:
            query = text("""
                         UPDATE books
                         SET (name, authors, user_id_taken, user_reserved_id, date_start_reserve, date_start_use, date_finish_use) = 
                         (:name, :authors, :user_id_taken, :user_reserved_id, :date_start_reserve, :date_start_use, :date_finish_use) 
                         WHERE id = :id
                         RETURNING *;
            """)
            result = await session.execute(query, book_schema.dict())
            result = result.one_or_none()
            if result:
                book = result
                await session.commit()
                return BookDBModel.from_orm(book)
            else:
                raise ValueError("Book not found.")
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_books(session: AsyncSession, offset_db: int | None = None, limit_db: int | None = None) -> BookDBModel | ErrorModel:
        try:
            result = session.execute(
                select(Books).offset(offset_db).limit(limit_db))
            result = result.all()
            users = [BookDBModel.from_orm(row) for row in result]
            return users
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
