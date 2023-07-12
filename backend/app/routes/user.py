from fastapi import APIRouter, Path, Depends
from typing import Annotated, Union

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tokens import AuthModel, Token
from app.schemas.users import UserDBModel, UserHashedModel, UserModel
from app.schemas.tokens import ButtonData, BigButtonData
from app.schemas.book_query import BookQueryModel, BookQueryDBModel
from app.schemas.error import ErrorModel

from app.core.security import get_password_hash

from app.core.db_conn import get_async_session

from app.crud.users import UserMethods

from app.methods.user import authenticate_user, take_book, cancel_take_book, reserve_book, cancel_reserve_book


class UserViews():

    user_routes = APIRouter(prefix="/user")

    @user_routes.post("/{user_id}/token", response_model=Union[Token, ErrorModel])
    async def login_for_access_token(user_id: Annotated[int, Path(title="id for user")],
                                     body: AuthModel, session: AsyncSession = Depends(get_async_session)):
        try:
            user = authenticate_user(body.email, body.password, user_id)
            if isinstance(user, ErrorModel):
                raise ("User not authenticated.")
            return Token(access_token=user.access_token,
                         token_type="bearer")
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_routes.post("/send_take", response_model=Union[BookQueryModel, ErrorModel])
    async def send_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await take_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_routes.post("/send_cancel_take", response_model=Union[BookQueryModel, ErrorModel])
    async def cancel_take_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await cancel_take_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_routes.post("/send_reserve", response_model=Union[BookQueryModel, ErrorModel])
    async def accept_reserve_view(body: ButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await reserve_book(body.user_id, body.book_id, session)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_routes.post("/cancel_reserve", response_model=Union[BookQueryDBModel, ErrorModel])
    async def cancel_reserve_view(body: BigButtonData, session: AsyncSession = Depends(get_async_session)):
        try:
            return await cancel_reserve_book(body.email, body.user_id, body.book_id, session)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))


class UsersDBViews():

    user_db_routes = APIRouter(prefix="/users")

    @user_db_routes.get("/action", response_model=Union[UserDBModel, ErrorModel])
    async def get_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
            result = await UserMethods.get_user_by_id(session, user_id)
            return result
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_db_routes.delete("/action", response_model=Union[UserHashedModel, ErrorModel])
    async def delete_user(user_id: int = 0, session: AsyncSession = Depends(get_async_session)):
        try:
            return await UserMethods.delete_user_by_id(session, user_id)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_db_routes.put("/action", response_model=Union[UserHashedModel, ErrorModel])
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
                hashed_password=get_password_hash(body.password)
            )
            return await UserMethods.create_user(session, current_schema)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @user_db_routes.post("/action", response_model=Union[UserHashedModel, ErrorModel])
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
                                         hashed_password=get_password_hash(
                                             body.password)
                                         )
            return await UserMethods.update_user(session, current_schema)
        except StatementError as database_error:
            
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
