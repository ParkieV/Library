from typing import List

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users
from app.schemas.users import UserDBModel, UserHashedModel


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> UserDBModel:
	query = text("""
					 SELECT *
					 FROM users
					 WHERE email = :user_email;
				""")

	result = await session.execute(query, {"user_email": email})

	if not (result := result.one_or_none()):
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	user = result
	await session.commit()
	return UserDBModel.from_orm(user)


async def create_user(session: AsyncSession, user_schema: UserHashedModel) -> UserHashedModel:
	user_model = Users(**user_schema.dict())

	session.add(user_model)

	await session.commit()
	return user_schema


async def get_user_by_id(session: AsyncSession, id: int) -> UserDBModel:
	query = text("""
					 SELECT *
					 FROM users
					 WHERE userId = :user_id;
				""")
	result = await session.execute(query, {"user_id": id})

	if not (result := result.one_or_none()):
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	user = result
	await session.commit()
	return UserDBModel.from_orm(user)


async def update_user(session: AsyncSession, user: UserDBModel) -> UserHashedModel:
	query = text("""
					UPDATE users
					SET (name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password) =
					(:name, :surname, :last_name, :email, :user_type, :book_id_taken, :reserved_book_id, :access_token, :time_token_create, :hashed_password)
					WHERE userId = :id
					RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;
			""")

	result = await session.execute(query, user.dict())

	if not (result := result.one_or_none()):
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	await session.commit()
	return UserHashedModel.from_orm(result)


async def delete_user_by_id(session: AsyncSession, id: int) -> UserHashedModel:
	query = text("""
					 DELETE FROM users
					 WHERE userId = :id
					 RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;
				""")

	result = await session.execute(query, {"id": id})

	if not (result := result.one_or_none()):
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	deleted_user = result
	await session.commit()
	return UserHashedModel.from_orm(deleted_user)


async def get_users(session: AsyncSession, db_offset: int | None = None, db_limit: int | None = None) -> List[UserDBModel]:
	result = await session.execute(select(Users).offset(db_offset).limit(db_limit))

	result = result.all()
	users = [UserDBModel.from_orm(row) for row in result]
	return users
