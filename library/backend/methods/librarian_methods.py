import json

from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from fastapi.responses import JSONResponse
from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.usersCRUD import UserMethods
from backend.crud.booksCRUD import BookMethods
from backend.crud.bookQueryCRUD import BookQueryMethods
from backend.schemas.users_schemas import UserDBModel
from backend.schemas.books_schemas import BookDBModel
from backend.schemas.book_query_schemas import BookQueryDBModel
from backend.schemas.error_schemas import ErrorModel
from backend.models.users import Users
from backend.models.books import Books


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
        await session.rollback()
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        await session.rollback()
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
        await session.rollback()
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        await session.rollback()
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
        await session.rollback()
        return ErrorModel(error_type=str(type(database_error).__name__),
                          error_details=database_error.orig)
    except Exception as err:
        await session.rollback()
        return ErrorModel(error_type=str(type(err).__name__),
                          error_details=str(err))

    user = json.loads(UserMethods.get_user_by_email(
        email).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(
        book_id).body.encode['utf-8'])["book"]
    if user["book_id_taken"] or book["user_id_taken"]:
        return JSONResponse(
            status_code=400,
            content={
                "details": "Uncorrect params"
            }
        )
    query = json.loads(BookQueryMethods.get_bookQuery_by_user_book(
        user_id, book_id).body.encode['utf-8'])["query"]
    try:
        changed_user = UserDBModel.parse_obj(user)
        changed_user.book_id_taken = None
        changed_user = Users(**changed_user.dict())
        UserMethods.update_user(changed_user)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    try:
        changed_book = BookDBModel.parse_obj(book)
        changed_book.user_id_taken = None
        changed_book.date_start_use = None
        changed_book.date_finish_use = None
        changed_book = Books(**changed_book.dict())
        BookMethods.update_book(changed_book)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    return BookQueryMethods.delete_bookQuery_by_id(query["id"])
