from pydantic import EmailStr
from datetime import timedelta, datetime
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import users as UserMethods
from app.crud import books as BookMethods
from app.crud import book_query as BookQueryMethods

from app.schemas.book_query import BookQueryModel, BookQueryDBModel
from app.schemas.users import UserDBModel

from app.core.security import verify_password, create_access_token
from app.core.settings import EnvJWTSettings



async def reserve_book(user_id: int, book_id: int, session: AsyncSession) -> BookQueryModel:
    ids = user, book = (await UserMethods.get_user_by_id(session, user_id), await BookMethods.get_book_by_id(session, book_id))
    
    match ids:
        case ids if user.book_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User has reserved a book")
        case ids if book.user_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Book has been reserved")
    
    query = BookQueryModel(
        user_id=user["id"],
        book_id=book["id"],
        type_order="Add",
        type_query="Reserve"
    )
    
    return await BookQueryMethods.create_book_query(session, query)


async def cancel_reserve_book(user_email: str, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel:
    ids = user, book = (await UserMethods.get_user_by_email(session, user_email), await BookMethods.get_book_by_id(session, book_id))
    
    match ids:
        case ids if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User id is uncorrect")
    
    query = await BookQueryMethods.get_book_query_by_user_book_id(ids[0].id, ids[1].id)
    
    user.reserved_book_id = None
    book.user_reserved_id = None
    
    await UserMethods.update_user(session, user)
    await BookMethods.update_book(session, book)
    
    return await BookQueryMethods.delete_book_query_by_id(session, query.id)


async def take_book(user_id: int, book_id: int, session: AsyncSession) -> BookQueryModel:
    ids = user, book = (await UserMethods.get_user_by_id(session, user_id), await BookMethods.get_book_by_id(session, book_id))
    
    match ids:
        case ids if user.book_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User has taken a book")
        case ids if book.user_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Book has been taken already")
    
    query = BookQueryModel(user_id=ids[0].id,
                           book_id=ids[1].id,
                           type_order="Cancel",
                           type_query="Take")
    
    return await BookQueryMethods.create_book_query(session, query)


async def cancel_take_book(user_id: int, book_id: int, session: AsyncSession) -> BookQueryModel:
    ids = user, book = (await UserMethods.get_user_by_id(session, user_id), await BookMethods.get_book_by_id(session, book_id))
    
    match ids:
        case ids if not user.book_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User hasn't take book.")
        case ids if not book.user_id_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Book hadn't taken by user.")
    
    query = BookQueryModel(user_id=ids[0].id,
                           book_id=ids[1].id,
                           type_order="Cancel",
                           type_query="Take")
    
    return await BookQueryMethods.create_book_query(session, query)


async def authenticate_user(email: EmailStr, password: str, id: int, session: AsyncSession) -> UserDBModel:
    user = await UserMethods.get_user_by_email(session, email, password)
    
    match user:
        case user if id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Id is uncorrect.")
        case user if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password is uncorrect.")
    
    jwt_settings = EnvJWTSettings()
    access_token_expires = timedelta(
        minutes=int(jwt_settings.token_expire_minutes))
    user.access_token = create_access_token(
        {"sub": user.email}, access_token_expires)
    user.time_token_create = datetime.now().isoformat()
    
    user = await UserMethods.update_user(user)
    
    return user
