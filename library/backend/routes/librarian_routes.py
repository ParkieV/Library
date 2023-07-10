import json

from typing import Union
from fastapi import APIRouter, Depends
from datetime import datetime

from fastapi.responses import JSONResponse
from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.methods.token_methods import PasswordJWT
from backend.crud.usersCRUD import UserMethods
from backend.schemas.users_schemas import BigButtonData
from backend.schemas.book_query_schemas import BookQueryDBModel
from backend.schemas.error_schemas import ErrorModel
from backend.methods.librarian_methods import accept_reserve_book, accept_take_book, cancel_take_book
from backend.core.db_settings import get_async_session


class LibrarianViews():
    
    librarian_router = APIRouter(prefix="/librarian")

    @librarian_router.post("/accept_reserve", response_model=Union[BookQueryDBModel, ErrorModel])
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
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @librarian_router.post("/accept_take", response_model=Union[BookQueryDBModel, ErrorModel])
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
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    @librarian_router.post("/cancel_take", response_model=Union[BookQueryDBModel, ErrorModel])
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
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_query = cancel_take_book(client["email"], body.data.user_id, body.data.book_id)
                response_query = json.loads(response_query.body.decode('utf-8'))
                response_query["access_token"] = token
                return JSONResponse(
                    content=response_query
                )