from fastapi import APIRouter, Path, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tokens import AuthModel, Token
from app.schemas.users import UserDBModel, UserHashedModel, UserModel
from app.schemas.tokens import ButtonData, BigButtonData
from app.schemas.book_query import BookQueryModel, BookQueryDBModel

from app.core.security import get_password_hash

from app.core.db_conn import get_async_session

from app.crud import users

from app.methods.user import authenticate_user, take_book, cancel_take_book, reserve_book, cancel_reserve_book


user_routes = APIRouter(prefix="/user")


@user_routes.post("/{user_id}/token", response_model=Token)
async def login_for_access_token(user_id: Annotated[int, Path(title="id for user")],
                                 body: AuthModel, session: AsyncSession = Depends(get_async_session)):
    
    user = authenticate_user(body.email, body.password, user_id, session)

    return Token(access_token=user.access_token,
                 token_type="bearer")


@user_routes.post("/send_take", response_model=BookQueryModel)
async def send_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
    return await take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_cancel_take", response_model=BookQueryModel)
async def cancel_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
    return await cancel_take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_reserve", response_model=BookQueryModel)
async def accept_reserve_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
    return await reserve_book(body.user_id, body.book_id, session)


@user_routes.post("/cancel_reserve", response_model=BookQueryDBModel)
async def cancel_reserve_view(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
    return await cancel_reserve_book(body.email, body.user_id, body.book_id, session)


user_db_routes = APIRouter(prefix="/users")


@user_db_routes.get("/action", response_model=UserDBModel)
async def get_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    result = await users.get_user_by_id(session, user_id)
    return result


@user_db_routes.delete("/action", response_model=UserHashedModel)
async def delete_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    return await users.delete_user_by_id(session, user_id)


@user_db_routes.put("/action", response_model=UserHashedModel)
async def create_user(body: UserModel, session: AsyncSession = Depends(get_async_session)):
    current_schema = UserHashedModel(
        name=body.name,
        surname=body.surname,
        last_name=body.last_name,
        email=body.email,
        user_type=body.user_type,
        book_id_taken=body.book_id_taken,
        reserved_book_id=body.reserved_book_id,
        access_token=body.access_token,
        time_token_create=body.time_token_create,
        hashed_password=get_password_hash(body.password))
    
    return await users.create_user(session, current_schema)


@user_db_routes.post("/action", response_model=UserHashedModel)
async def update_user(body: UserModel, user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    current_schema = UserDBModel(id=user_id,
                                 name=body.name,
                                 surname=body.surname,
                                 last_name=body.last_name,
                                 email=body.email,
                                 user_type=body.user_type,
                                 book_id_taken=body.book_id_taken,
                                 reserved_book_id=body.reserved_book_id,
                                 access_token=body.access_token,
                                 time_token_create=body.time_token_create,
                                 hashed_password=get_password_hash(body.password))
    
    return await users.update_user(session, current_schema)
