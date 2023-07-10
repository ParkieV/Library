from fastapi import APIRouter, Depends
from typing import Union

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.book_query_schemas import BookQueryDBModel, BookQueryModel
from backend.schemas.error_schemas import ErrorModel
from backend.crud.bookQueryCRUD import BookQueryMethods
from backend.core.db_settings import get_async_session


class BookQueriesDBViews():

    queries_router = APIRouter(prefix="/queries")

    @queries_router.get("/action", response_model=Union[BookQueryDBModel, ErrorModel])
    async def get_query(query_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
            return await BookQueryMethods.get_book_query_by_id(session, query_id)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @queries_router.put("/action", response_model=Union[BookQueryModel, ErrorModel])
    async def create_query(body: BookQueryModel, session: AsyncSession = Depends(get_async_session)):
        try:
            return await BookQueryMethods.create_book_query(session, body)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @queries_router.delete("/action", response_model=Union[BookQueryDBModel, ErrorModel])
    async def delete_query(query_id: int, session: AsyncSession = Depends(get_async_session)):
        try:
            return await BookQueryMethods.delete_book_query_by_id(session, query_id)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
        