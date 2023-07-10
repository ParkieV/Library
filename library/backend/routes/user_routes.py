import json

from fastapi import APIRouter, Path, Depends
from typing import Annotated, Union
from datetime import datetime

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.tokens_schemas import AuthModel, Token
from backend.schemas.users_schemas import UserDBModel, UserHashedModel, UserModel, ButtonData, BigButtonData
from backend.schemas.book_query_schemas import BookQueryModel, BookQueryDBModel
from backend.schemas.error_schemas import ErrorModel
from backend.methods.token_methods import PasswordJWT
from backend.core.db_settings import get_async_session
from backend.crud.usersCRUD import UserMethods
from backend.methods.user_methods import authenticate_user, take_book, cancel_take_book, reserve_book, cancel_reserve_book


class UserViews():

    user_router = APIRouter(prefix="/user")

    @user_router.post("/{user_id}/token", response_model=Union[Token, ErrorModel])
    async def login_for_access_token(user_id: Annotated[int, Path(title="id for user")],\
                                     body: AuthModel, session: AsyncSession = Depends(get_async_session)):
        try:
            user = authenticate_user(body.email, body.password, user_id)
            if isinstance(user, ErrorModel):
                raise("User not authenticated.")
            return Token(access_token=user.access_token,
                         token_type="bearer")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_router.post("/send_take", response_model=Union[BookQueryModel, ErrorModel])
    async def send_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await take_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
    
    @user_router.post("/send_cancel_take", response_model=Union[BookQueryModel, ErrorModel])
    async def cancel_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await cancel_take_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_router.post("/send_reserve", response_model=Union[BookQueryModel, ErrorModel])
    async def accept_reserve_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await reserve_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_router.post("/cancel_reserve", response_model=Union[BookQueryDBModel, ErrorModel])
    async def cancel_reserve_view(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await cancel_reserve_book(body.email, body.user_id, body.book_id, session)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))


class UsersDBViews():

    users_router = APIRouter(prefix="/users")

    @users_router.get("/action", response_model=Union[UserDBModel, ErrorModel])
    async def get_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
            result = await UserMethods.get_user_by_id(session, user_id)
            return result
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @users_router.delete("/action", response_model=Union[UserHashedModel, ErrorModel])
    async def delete_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
            return await UserMethods.delete_user_by_id(session, user_id)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @users_router.put("/action", response_model=Union[UserHashedModel, ErrorModel])
    async def create_user(body: UserModel, session: AsyncSession = Depends(get_async_session)):
        try:
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
                hashed_password=PasswordJWT.get_password_hash(body.password)
            )
            return await UserMethods.create_user(session, current_schema)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @users_router.post("/action", response_model=Union[UserHashedModel, ErrorModel])
    async def update_user(body: UserModel, user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
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
                                         hashed_password=PasswordJWT.get_password_hash(
                                             body.password)
                                         )
            return await UserMethods.update_user(session, current_schema)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
