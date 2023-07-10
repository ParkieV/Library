from typing import List
from sqlalchemy import text, select
from pydantic import EmailStr

from sqlalchemy.exc import StatementError

from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users_schemas import UserDBModel, UserHashedModel
from backend.schemas.tokens_schemas import AuthModel
from backend.schemas.error_schemas import ErrorModel
from backend.models.users import Users



class UserMethods():

    async def get_user_by_email(session: AsyncSession, email: EmailStr) -> UserDBModel | ErrorModel:
        try:
            query = text("""
                         SELECT *
                         FROM users
                         WHERE email = :user_email;
                    """)
            result = await session.execute(query, {"user_email": email})
            result = result.one_or_none()
            if result:
                raise ValueError("User not found.")
            else:                
                user = result
                await session.commit()
                return UserDBModel.from_orm(user)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def create_user(session: AsyncSession, user_schema: UserHashedModel) -> UserHashedModel | ErrorModel:
        try:
            user_model = Users(**user_schema.dict())
            session.add(user_model)
            await session.commit()
            return user_schema
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_user_by_id(session: AsyncSession, id: int) -> UserDBModel | ErrorModel:
        try:
            query = text("""
                         SELECT *
                         FROM users
                         WHERE id = :user_id;                    
                    """)
            result = await session.execute(query, {"user_id": id})
            result = result.one_or_none()
            if result:
                user = result
                await session.commit()
                return UserDBModel.from_orm(user)
            else:
                raise ValueError("User not found.")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def update_user(session: AsyncSession, user: UserDBModel) -> UserHashedModel | ErrorModel:
        try:
            query = text("""
                         UPDATE users
                         SET (name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password) = 
                         (:name, :surname, :last_name, :email, :user_type, :book_id_taken, :reserved_book_id, :access_token, :time_token_create, :hashed_password)
                         WHERE id = :id
                         RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;
                """)
            result = await session.execute(query, user.dict())
            result = result.one_or_none()
            if result:
                user = result
                await session.commit()
                return UserHashedModel.from_orm(user)
            else:
                raise ValueError("User hasn't updated")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def delete_user_by_id(session: AsyncSession, id: int) -> UserHashedModel | ErrorModel:
        try:
            query = text("""
                         DELETE FROM users
                         WHERE id = :id
                         RETURNING name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password;                           
                    """)
            result = await session.execute(query, {"id": id})
            result = result.one_or_none()
            if result:
                print(result)
                deleted_user = result
                await session.commit()
                return UserHashedModel.from_orm(deleted_user)
            else:
                raise ValueError("User hasn't deleted.")
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_user_by_email_password(session: AsyncSession, auth_schema: AuthModel) -> UserHashedModel | ErrorModel:
        try:
            query = text(
                """
                SELECT *
                FROM users
                WHERE email = :user_email
                AND password = :user_password;
            """)
            result = await session.execute(query, auth_schema.dict())
            result = result.one_or_none()
            if result:
                raise ValueError("User not found.")
            else:
                user = result
                session.commit()
                return UserHashedModel.from_orm(user)
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))

    async def get_users(session: AsyncSession, db_offset: int | None = None, db_limit: int | None = None) -> List[UserHashedModel] | ErrorModel:
        try:
            result = await session.execute(select(Users).offset(db_offset).limit(db_limit))
            result = result.all()
            users = [UserHashedModel.from_orm(row) for row in result]
            return users
        except StatementError as database_error:
            await session.rollback()
            return ErrorModel(error_type=str(type(database_error).__name__),
                              error_details=database_error.orig)
        except Exception as err:
            await session.rollback()
            return ErrorModel(error_type=str(type(err).__name__),
                              error_details=str(err))
