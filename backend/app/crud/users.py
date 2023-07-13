from typing import List
from sqlalchemy import text, select
from pydantic import EmailStr
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import UserDBModel, UserHashedModel
from app.schemas.tokens import AuthModel

from app.models.users import Users


class UserMethods():

    async def get_user_by_email(session: AsyncSession, email: EmailStr) -> UserDBModel:
        query = text("""
                     SELECT *
                     FROM users
                     WHERE email = :user_email;
                """)
        
        result = await session.execute(query, {"user_email": email})

        if result := result.one_or_none():
            user = result
            await session.commit()
            return UserDBModel.from_orm(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def create_user(session: AsyncSession, user_schema: UserHashedModel) -> UserHashedModel:
        user_model = Users(**user_schema.dict())

        session.add(user_model)
        
        await session.commit()
        return user_schema

    async def get_user_by_id(session: AsyncSession, id: int) -> UserDBModel:
        query = text("""
                     SELECT *
                     FROM users
                     WHERE id = :user_id;                    
                """)
        result = await session.execute(query, {"user_id": id})

        if result := result.one_or_none():
            user = result
            await session.commit()
            return UserDBModel.from_orm(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def update_user(session: AsyncSession, user: UserDBModel) -> UserHashedModel:
        query = text("""
                     UPDATE users
                     SET (name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password) = 
                     (:name, :surname, :last_name, :email, :user_type, :book_id_taken, :reserved_book_id, :access_token, :time_token_create, :hashed_password)
                     WHERE id = :id
                     RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;
            """)

        result = await session.execute(query, user.dict())
        
        if result := result.one_or_none():
            user = result
            await session.commit()
            return UserHashedModel.from_orm(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def delete_user_by_id(session: AsyncSession, id: int) -> UserHashedModel:
        query = text("""
                     DELETE FROM users
                     WHERE id = :id
                     RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;                           
                """)
        
        result = await session.execute(query, {"id": id})
        
        if result := result.one_or_none():
            deleted_user = result
            await session.commit()
            return UserHashedModel.from_orm(deleted_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def get_user_by_email_password(session: AsyncSession, auth_schema: AuthModel) -> UserHashedModel:
        query = text(
            """
            SELECT *
            FROM users
            WHERE email = :user_email
            AND password = :user_password;
        """)
        
        result = await session.execute(query, auth_schema.dict())
        
        if result := result.one_or_none():
            user = result
            session.commit()
            return UserHashedModel.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def get_users(session: AsyncSession, db_offset: int | None = None, db_limit: int | None = None) -> List[UserHashedModel]:
            result = await session.execute(select(Users).offset(db_offset).limit(db_limit))

            result = result.all()
            users = [UserHashedModel.from_orm(row) for row in result]
            return users
                    