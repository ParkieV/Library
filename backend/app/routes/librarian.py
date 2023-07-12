
from typing import Union
from fastapi import APIRouter, Depends

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UserMethods
from app.schemas.tokens import BigButtonData
from app.schemas.book_query import BookQueryDBModel
from app.schemas.error import ErrorModel
from app.methods.librarian import accept_reserve_book, accept_take_book, cancel_take_book
from app.core.db_conn import get_async_session


routes = APIRouter(prefix="/librarian")


@routes.post("/accept_reserve", response_model=Union[BookQueryDBModel, ErrorModel])
async def accept_reserve_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await UserMethods.get_user_by_id(body.user_id)
        match user:
            case user if isinstance(user, ErrorModel):
                raise ValueError("User id is uncorrect.")
            case user if user.user_type != "Librarian":
                raise ValueError("User is not a librarian.")
        return await accept_reserve_book(body.email, body.user_id, body.book_id, session)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.post("/accept_take", response_model=Union[BookQueryDBModel, ErrorModel])
async def accept_take_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await UserMethods.get_user_by_id(body.user_id)
        match user:
            case user if isinstance(user, ErrorModel):
                raise ValueError("User id is uncorrect.")
            case user if user.user_type != "Librarian":
                raise ValueError("User is not a librarian.")
        return await accept_take_book(body.email, body.user_id, body.book_id, session)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


@routes.post("/cancel_take", response_model=Union[BookQueryDBModel, ErrorModel])
async def cancel_take_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await UserMethods.get_user_by_id(body.user_id)
        match user:
            case user if isinstance(user, ErrorModel):
                raise ValueError("User id is uncorrect.")
            case user if user.user_type != "Librarian":
                raise ValueError("User is not a librarian.")
        return await cancel_take_book(body.email, body.user_id, body.book_id, session)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))
