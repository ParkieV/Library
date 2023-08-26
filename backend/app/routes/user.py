from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.core.security import get_password_hash
from app.crud import users
from app.methods.user import (
	cancel_reserve_book,
	cancel_take_book,
	reserve_book,
	take_book,
)
from app.schemas.book_query import (
	BookQueryDBModel,
	BookQueryModel,
	QueryActionModel,
	UserQueryActionModel,
)
from app.schemas.users import UserDBModel, UserHashedModel, UserModel

user_routes = APIRouter(prefix="/user")


@user_routes.post("/send_take", response_model=BookQueryModel)
async def send_take_view(body: QueryActionModel,
						session: AsyncSession = Depends(get_async_session)):

	return await take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_cancel_take", response_model=BookQueryModel)
async def cancel_take_view(body: QueryActionModel,
						session: AsyncSession = Depends(get_async_session)):

	return await cancel_take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_reserve", response_model=BookQueryModel)
async def accept_reserve_view(body: QueryActionModel,
							session: AsyncSession = Depends(get_async_session)):  # noqa: E101, E501

	return await reserve_book(body.user_id, body.book_id, session)


@user_routes.post("/cancel_reserve", response_model=BookQueryDBModel)
async def cancel_reserve_view(body: UserQueryActionModel,
							session: AsyncSession = Depends(get_async_session)):

	return await cancel_reserve_book(body.email, body.user_id, body.book_id, session)


user_db_routes = APIRouter(prefix="/users")


@user_db_routes.get("/action", response_model=UserDBModel)
async def get_user(user_id: int = 0,
				session: AsyncSession = Depends(get_async_session)):

	result = await users.get_user_by_id(session, user_id)
	return result


@user_db_routes.delete("/action", response_model=UserHashedModel)
async def delete_user(user_id: int = 0,
					session: AsyncSession = Depends(get_async_session)):

	return await users.delete_user_by_id(session, user_id)


@user_db_routes.put("/action", response_model=UserHashedModel)
async def create_user(body: UserModel,
				session: AsyncSession = Depends(get_async_session)):

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
async def update_user(body: UserModel, user_id: int = 0,
					session: AsyncSession = Depends(get_async_session)):

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


@user_db_routes.get("get_users", response_model= List[UserDBModel] | None)
async def get_users_view(page: int,
						session: AsyncSession = Depends(get_async_session)) -> List[UserDBModel] | None:  # noqa: E501

	result = await users.get_users(session, page*15)
	return result
