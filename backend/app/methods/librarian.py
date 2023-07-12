import json

from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UserMethods
from app.crud.books import BookMethods
from app.crud.book_query import BookQueryMethods
from app.schemas.book_query import BookQueryDBModel
from app.schemas.error import ErrorModel


async def accept_reserve_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel | ErrorModel:
    try:
        ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)
        match ids:
            case ids if user.id != user_id:
                raise ValueError("User id is uncorrect.")
            case ids if isinstance(book, ErrorModel):
                raise ValueError("Book id is uncorrect.")
            case ids if user.reserved_book_id:
                raise ValueError("User reserved book.")
            case ids if book.user_reserved_id:
                raise ValueError("Book has reserved.")
        query = BookQueryMethods.get_book_query_by_user_book_id(
            session, user.id, book.id)
        if isinstance(query, ErrorModel):
            raise ValueError("Query not found.")
        user.reserved_book_id = book_id
        book.user_reserved_id = user_id
        await UserMethods.update_user(session, user)
        await BookMethods.create_book(session, book)
        return await BookQueryMethods.delete_book_query_by_id(session, query.id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


async def accept_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession,
                           date_finish=datetime.now(timezone.utc) + timedelta(days=31)) -> BookQueryDBModel | ErrorModel:
    try:
        ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)
        match ids:
            case ids if user.id != user_id:
                raise ValueError("User id is uncorrect.")
            case ids if isinstance(book, ErrorModel):
                raise ValueError("Book id is uncorrect.")
            case ids if user.reserved_book_id:
                raise ValueError("User reserved book.")
            case ids if book.user_reserved_id:
                raise ValueError("Book has reserved.")
        query = BookQueryMethods.get_book_query_by_user_book_id(
            session, user.id, book.id)
        if isinstance(query, ErrorModel):
            raise ValueError("Query not found.")
        user.book_id_taken = book_id
        book.user_id_taken = user_id
        book.date_start_use = datetime.now()
        book.date_finish_use = date_finish
        await UserMethods.update_user(session, user)
        await BookMethods.create_book(session, book)
        return await BookQueryMethods.delete_book_query_by_id(session, query.id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))


async def cancel_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel | ErrorModel:
    try:
        ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)
        match ids:
            case ids if user.id != user_id:
                raise ValueError("User id is uncorrect.")
            case ids if isinstance(book, ErrorModel):
                raise ValueError("Book id is uncorrect.")
            case ids if user.reserved_book_id:
                raise ValueError("User reserved book.")
            case ids if book.user_reserved_id:
                raise ValueError("Book has reserved.")
        query = BookQueryMethods.get_book_query_by_user_book_id(
            session, user.id, book.id)
        if isinstance(query, ErrorModel):
            raise ValueError("Query not found.")
        user.book_id_taken = None
        book.user_id_taken = None
        book.date_start_use = None
        book.date_finish_use = None
        await UserMethods.update_user(session, user)
        await BookMethods.create_book(session, book)
        return await BookQueryMethods.delete_book_query_by_id(session, query.id)
    except StatementError as database_error:
        
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))
