from typing import List
from sqlalchemy import text, select

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.bookQuery import BookQuery
from backend.schemas.book_query_schemas import BookQueryDBModel, BookQueryModel
from backend.schemas.error_schemas import ErrorModel


class BookQueryMethods():

    async def get_book_query_by_id(session: AsyncSession, book_query_id: int) -> BookQueryDBModel | ErrorModel:
        try:
            query = text("""
                         SELECT *
                         FROM book_queries
                         WHERE id = :id;
                    """)
            result = await session.execute(query, {"id": book_query_id})
            result = result.one_or_none()
            if result:
                book_query = result
                await session.commit()
                return BookQueryDBModel.from_orm(book_query)
            else:
                raise ValueError("Book query not found.")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_book_query_by_user_book_id(session: AsyncSession, user_id: int, book_id: int) -> BookQueryDBModel | ErrorModel:
        try:
            query = text("""
                SELECT *
                FROM book_queries
                WHERE user_id = :user_id 
                AND book_id = :book_id;
            """)
            result = await session.execute(query, {"user_id": user_id, "book_id": book_id})
            result = result.one_or_none()
            if result:
                    book_query = result
                    await session.commit()
                    return BookQueryDBModel.from_orm(book_query)
            else:
                raise ValueError("Book query not found.")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def create_book_query(session: AsyncSession, book_query_schema: BookQueryModel) -> BookQueryModel | ErrorModel:
        try:
            book_query_model = BookQuery(**book_query_schema.dict())
            session.add(book_query_model)
            await session.commit()
            return book_query_schema
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def delete_book_query_by_id(session: AsyncSession, book_query_id: int) -> BookQueryDBModel | ErrorModel:
        try:
            query = text("""
                         DELETE FROM book_queries
                         WHERE id = :id
                         RETURNING *;
                    """)
            result = await session.execute(query, {"id": book_query_id})
            result = result.one_or_none()
            if result:
                book_query = result
                await session.commit()
                return BookQueryDBModel.from_orm(book_query)
            else:
                raise ValueError("Book query not found.")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_book_queries(session: AsyncSession, offset_db : int | None = None, limit_db : int | None = None) -> List[BookQueryDBModel] | ErrorModel:
        try:
            result = await session.execute(select(BookQuery).offset(offset_db).limit(limit_db))
            result = result.all()
            book_queries = await [BookQueryDBModel.from_orm(row) for row in result]
            return book_queries
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
