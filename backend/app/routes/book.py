from fastapi import APIRouter, Depends
from typing import Union

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.books import BookModel, BookDBModel
from app.schemas.error import ErrorModel
from app.crud.books import BookMethods
from app.core.db_conn import get_async_session


routes = APIRouter(prefix="/books")


@routes.get("/action", response_model=Union[BookDBModel, ErrorModel])
async def get_book(book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookMethods.get_book_by_id(session, book_id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.post("/action", response_model=Union[BookDBModel, ErrorModel])
async def update_book(body: BookModel, book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        current_schema = BookDBModel(id=book_id,
                                     name=body.name,
                                     authors=body.authors,
                                     user_id_taken=body.user_id_taken,
                                     user_reserved_id=body.user_reserved_id,
                                     date_start_reserve=body.date_start_reserve,
                                     date_start_use=body.date_finish_use,
                                     date_finish_use=body.date_finish_use)
        return await BookMethods.update_book(session, current_schema)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.put("/action", response_model=Union[BookModel, ErrorModel])
async def create_book(body: BookModel, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookMethods.create_book(session, body)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.delete("/action", response_model=Union[BookDBModel, ErrorModel])
async def delete_book(book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        return await BookMethods.delete_book_by_id(session, book_id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))
