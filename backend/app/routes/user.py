from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.core.security import get_password_hash
from app.crud import users
from app.methods.tokens import checkAccess
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
async def send_take_view(body: QueryActionModel, check_access: None = Depends(checkAccess),
						session: AsyncSession = Depends(get_async_session)):

	if check_access == "Anonymous":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

	return await take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_cancel_take", response_model=BookQueryModel)
async def cancel_take_view(body: QueryActionModel, check_access: None = Depends(checkAccess),
						session: AsyncSession = Depends(get_async_session)):

	if check_access == "Anonymous":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

	return await cancel_take_book(body.user_id, body.book_id, session)


@user_routes.post("/send_reserve", response_model=BookQueryModel)
async def accept_reserve_view(body: QueryActionModel, check_access: None = Depends(checkAccess),
							session: AsyncSession = Depends(get_async_session)):

	if check_access == "Anonymous":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

	return await reserve_book(body.user_id, body.book_id, session)


@user_routes.post("/cancel_reserve", response_model=BookQueryDBModel)
async def cancel_reserve_view(body: UserQueryActionModel, check_access: None = Depends(checkAccess),
							session: AsyncSession = Depends(get_async_session)):

	if check_access == "Anonymous":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized")

	return await cancel_reserve_book(body.email, body.user_id, body.book_id, session)


user_db_routes = APIRouter(prefix="/users")


@user_db_routes.get("/action", response_model=UserDBModel)
async def get_user(user_id: int = 0, check_access: None = Depends(checkAccess),
		session: AsyncSession = Depends(get_async_session)):

	result = await users.get_user_by_id(session, user_id)
	return result


@user_db_routes.delete("/action", response_model=UserHashedModel)
async def delete_user(user_id: int = 0, check_access: None = Depends(checkAccess),
					session: AsyncSession = Depends(get_async_session)):

	return await users.delete_user_by_id(session, user_id)


@user_db_routes.put("/action", response_model=UserHashedModel)
async def create_user(body: UserModel, check_access: None = Depends(checkAccess),
				session: AsyncSession = Depends(get_async_session)):

	current_schema = UserHashedModel(hashed_password=get_password_hash(body.password),
				  **body.dict())

	return await users.create_user(session, current_schema)


@user_db_routes.post("/action", response_model=UserHashedModel)
async def update_user(body: UserModel, user_id: int = 0, check_access: None = Depends(checkAccess),
					session: AsyncSession = Depends(get_async_session)):

	current_schema = UserDBModel(userId=user_id,
								hashed_password=get_password_hash(body.password),
								**body.dict())

	return await users.update_user(session, current_schema)

