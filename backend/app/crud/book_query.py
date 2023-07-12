from typing import List
from sqlalchemy import text, select
from fastapi import status

from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException


from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_query import BookQuery

from app.schemas.book_query import BookQueryDBModel, BookQueryModel
from app.schemas.error import ErrorModel


class BookQueryMethods():

    async def get_book_query_by_id(session: AsyncSession, book_query_id: int) -> BookQueryDBModel | HTTPException:
        query = text("""
                     SELECT *
                     FROM book_queries
                     WHERE id = :id;
                """)
        
        try:
            result = await session.execute(query, {"id": book_query_id})

            if not (result := result.one_or_none()):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            
            result = result.one_or_none()
            book_query = result
            await session.commit()
            return BookQueryDBModel.from_orm(book_query)
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def get_book_query_by_user_book_id(session: AsyncSession, user_id: int, book_id: int) -> BookQueryDBModel | HTTPException:
        query = text("""
            SELECT *
            FROM book_queries
            WHERE user_id = :user_id 
            AND book_id = :book_id;
        """)

        try:
            result = await session.execute(query, {"user_id": user_id, "book_id": book_id})

            if not (result := result.one_or_none()):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            
            result = result.one_or_none()
            book_query = result
            await session.commit()
            return BookQueryDBModel.from_orm(book_query)
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def create_book_query(session: AsyncSession, book_query_schema: BookQueryModel) -> BookQueryModel | HTTPException:
        try:
            book_query_model = BookQuery(**book_query_schema.dict())
            session.add(book_query_model)
            await session.commit()
            return book_query_schema
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def delete_book_query_by_id(session: AsyncSession, book_query_id: int) -> BookQueryDBModel | HTTPException:
        query = text("""
                     DELETE FROM book_queries
                     WHERE id = :id
                     RETURNING *;
                """)
        
        try:
            result = await session.execute(query, {"id": book_query_id})

            if not (result := result.one_or_none()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book query not found")
            
            result = result.one_or_none()
            book_query = result
            await session.commit()
            return BookQueryDBModel.from_orm(book_query)
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    async def get_book_queries(session: AsyncSession, offset_db: int | None = None, limit_db: int | None = None) -> List[BookQueryDBModel] | ErrorModel:
        try:
            result = await session.execute(select(BookQuery).offset(offset_db).limit(limit_db))
            
            result = result.all()
            book_queries = await [BookQueryDBModel.from_orm(row) for row in result]
            return book_queries
        
        except IntegrityError as database_error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=sql_validation_error(database_error))

        except Exception as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
