from fastapi import APIRouter, Depends, HTTPException, status


from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import users

from app.schemas.tokens import BigButtonData
from app.schemas.book_query import BookQueryDBModel

from app.methods.librarian import accept_reserve_book, accept_take_book, cancel_take_book

from app.core.db_conn import get_async_session


routes = APIRouter(prefix="/librarian")


@routes.post("/accept_reserve", response_model=BookQueryDBModel)
async def accept_reserve_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    user = await users.get_user_by_id(body.user_id)
    match user:
        case user if user.user_type != "Librarian":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian.")

    return await accept_reserve_book(body.email, body.user_id, body.book_id, session)


@routes.post("/accept_take", response_model=BookQueryDBModel)
async def accept_take_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    user = await users.get_user_by_id(body.user_id)
    match user:
        case user if user.user_type != "Librarian":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian.")

    return await accept_take_book(body.email, body.user_id, body.book_id, session)


@routes.post("/cancel_take", response_model=BookQueryDBModel)
async def cancel_take_query(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    user = await users.get_user_by_id(body.user_id)
    match user:
        case user if user.user_type != "Librarian":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian.")

    return await cancel_take_book(body.email, body.user_id, body.book_id, session)
