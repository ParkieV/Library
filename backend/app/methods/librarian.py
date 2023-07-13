from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from fastapi import HTTPException, status


from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import users as UserMethods
from app.crud import books as BookMethods
from app.crud import book_query as BookQueryMethods

from app.schemas.book_query import BookQueryDBModel


async def accept_reserve_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel:
    ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)

    match ids:
        case ids if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User id is uncorrect")
        case ids if user.reserved_book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User reserved book")
        case ids if book.user_reserved_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Book has reserved")

    query = BookQueryMethods.get_book_query_by_user_book_id(
        session, user.id, book.id)

    user.reserved_book_id = book_id
    book.user_reserved_id = user_id

    await UserMethods.update_user(session, user)
    await BookMethods.create_book(session, book)
    
    return await BookQueryMethods.delete_book_query_by_id(session, query.id)


async def accept_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession,
                           date_finish=datetime.now(timezone.utc) + timedelta(days=31)) -> BookQueryDBModel:
    ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)

    match ids:
        case ids if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User id is uncorrect")
        case ids if user.reserved_book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User reserved book")
        case ids if book.user_reserved_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Book has reserved")

    query = BookQueryMethods.get_book_query_by_user_book_id(
        session, user.id, book.id)

    user.book_id_taken = book_id
    book.user_id_taken = user_id
    book.date_start_use = datetime.now()
    book.date_finish_use = date_finish

    await UserMethods.update_user(session, user)
    await BookMethods.create_book(session, book)
    
    return await BookQueryMethods.delete_book_query_by_id(session, query.id)


async def cancel_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel:
        ids = user, book = await UserMethods.get_user_by_email(session, email), await BookMethods.get_book_by_id(session, book_id)

        match ids:
            case ids if user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User id is uncorrect")
            case ids if user.reserved_book_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User reserved book")
            case ids if book.user_reserved_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Book has reserved")

        query = BookQueryMethods.get_book_query_by_user_book_id(
            session, user.id, book.id)

        user.book_id_taken = None
        book.user_id_taken = None
        book.date_start_use = None
        book.date_finish_use = None

        await UserMethods.update_user(session, user)
        await BookMethods.create_book(session, book)
        
        return await BookQueryMethods.delete_book_query_by_id(session, query.id)
