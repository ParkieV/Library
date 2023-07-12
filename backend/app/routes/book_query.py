from fastapi import APIRouter, Depends
from typing import Union

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.book_query import BookQueryDBModel, BookQueryModel
from app.schemas.error import ErrorModel
from app.crud.book_query import BookQueryMethods
from app.core.db_conn import get_async_session


routes = APIRouter(prefix="/queries")


@routes.get("/action", response_model=Union[BookQueryDBModel, ErrorModel])
async def get_query(query_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookQueryMethods.get_book_query_by_id(session, query_id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.put("/action", response_model=Union[BookQueryModel, ErrorModel])
async def create_query(body: BookQueryModel, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookQueryMethods.create_book_query(session, body)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.delete("/action", response_model=Union[BookQueryDBModel, ErrorModel])
async def delete_query(query_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookQueryMethods.delete_book_query_by_id(session, query_id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))
