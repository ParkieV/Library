import json

from sqlalchemy import create_engine, text, CursorResult
from pydantic import EmailStr
from typing import List, Annotated
from datetime import datetime, timedelta, date, timezone
from dateutil import parser
from jose import JWTError, jwt
from fastapi import Depends

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.db.schema import UserDBModel, BookDBModel, AuthModel
from backend.db.schema import TokenData
from backend.db.models import Users, Books, BookQuery
from backend.db.settings import DBSettings, JWTSettings


class UserMethods():
    def setUp(func) -> None:
        def _wrapper(*args, **kwargs):
            settings = DBSettings()
            engine = create_engine(f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}")
            session = Session(bind=engine)
            kwargs['session'] = session
            result = func(*args, **kwargs)
            session.commit()
            session.close()
            return result
        return _wrapper

    @setUp
    def get_user_by_email(email: EmailStr, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]

        query = text("""
            SELECT *
            FROM users
            WHERE email = :user_email;
        """)
        result = session.execute(query, {"user_email": email}).mappings().first()
        response = CursorResultDict(result)
        response["time_token_create"] = json.dumps(response["time_token_create"], default=json_serial)
        if result:
            return JSONResponse(
                status_code = 200,
                content={
                    "user": response
                }
                
            )
        return JSONResponse(
            status_code = 500,
            content={
                "details": 'User not found.'
            }
            
        )
    
    @setUp
    def create_user(model: Users, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        try:
            session.add(model)
        except Exception as err:
            return JSONResponse(
                status_code = 500,
                content={
                  "details": str(err) + ". Operation is unavailable.",  
                }
            )
        return JSONResponse(
            content={
                "details": 'OK'
            }
        )

    @setUp
    def get_user_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs['session']
        query = text("""
            SELECT *
            FROM users
            WHERE id = :user_id;
        """)
        result = session.execute(query, {"user_id": id}).mappings().first()
        response = CursorResultDict(result)
        response["time_token_create"] = json.dumps(response["time_token_create"], default=json_serial)
        user_model = {
            "id": response["id"],
        "name": response["name"],
        "surname": response["surname"],
        "last_name": response["last_name"],
        "email": response["email"],
        "hashed_password": response["hashed_password"],
        "user_type": response["user_type"],
        "book_id_taken": response["book_id_taken"],
        "reserved_book_id": response["reserved_book_id"],
        }
        if result:
            return JSONResponse(
                content={
                        "user": user_model
                }
            )
        else:
            return JSONResponse(
                status_code = 404,
                content = {
                "details": 'User not found'
                }
            )

    async def get_current_user(token: Annotated[str, Depends(PasswordJWT.oauth2_scheme)]) -> JSONResponse:
        credentials_exception = JSONResponse(
            status_code=401,
            content={
                "details": "Could not validate credentials"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, PasswordJWT.settings.SECRET_KEY, algorithms=[PasswordJWT.settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = UserMethods.get_user_by_email(email)
        if user.status_code != 200:
            raise credentials_exception
        return user
    
    async def get_current_active_user(
        current_user: Annotated[JSONResponse, Depends(get_current_user)]
    ):
        if current_user.status_code != 200:
            return current_user
        current_user = json.loads(current_user.body.encode["utf-8"])["user"]
        if current_user["disabled"]:
            raise JSONResponse(contents={"details": "Inactive user"})
        return current_user
    
    @setUp
    def update_user(model: UserDBModel, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        try:
            query = text("""
                UPDATE users
                SET (name, surname, last_name, email, user_type, book_id_taken, reserved_book_id, access_token, time_token_create, hashed_password) = 
                (:name, :surname, :last_name, :email, :user_type, :book_id_taken, :reserved_book_id, :access_token, :time_token_create, :hashed_password)
                WHERE id = :id;
            """)
            session.execute(query, {
                "name": model.name,
                "surname": model.surname,
                "last_name": model.last_name,
                "email": model.email,
                "user_type": model.user_type,
                "book_id_taken": model.book_id_taken,
                "reserved_book_id": model.reserved_book_id,
                "access_token": model.access_token,
                "time_token_create": model.time_token_create,
                "hashed_password": model.hashed_password,
                "id": model.id
            })
            return JSONResponse(
                content={
                    "details": "OK"
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable.",
                }
            )

    @setUp
    def delete_user_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs['session']
        user = UserMethods.get_user_by_id(id)
        if user.status_code != 200:
            return user
        try:
            query = text("""
                DELETE FROM users
                WHERE id = :id;
            """)
            session.execute(query, {
                "id": id
            })
            return JSONResponse(
                content={
                    "details": 'OK'
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code = 500,
                content={
                    "details": str(err) + " . Operation is unavailable."
                }
            )

    @setUp
    def get_user_by_email_password(model: AuthModel, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        if not UserMethods._auth_validation(model.email, model.password):
            return JSONResponse(
                status_code = 400,
                content = {
                    "details": "Invalid email or password"
                }
            )
        try:
            query = text(
                """
                SELECT *
                FROM users
                WHERE email = :user_email
                AND password = :user_password;
            """)
            result = session.execute(query, 
                                     {"user_email": model.email, "user_password": model.password}).mappings().all()
            if len(result) != 1:
                return JSONResponse(
                    status_code = 404,
                    content = {
                    "details": "User not found"
                    }
                )
            result = result[0]
            return JSONResponse(
                content={
                    "user": CursorResultDict(result)
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code = 500,
                content = {
                    "details": str(err) + ". Operation is unavailable"
                }
            )

    @setUp
    def get_database(offset: int = 0, limit: int = 15, *args, **kwargs) ->JSONResponse:
        session = kwargs["session"]
        if limit == 0:
            try: 
                query = text(
                    """
                    SELECT *
                    FROM users;
                """)
                result = session.execute(query).mappings().all()
                result_dict = CursorResultDict(result)
                return JSONResponse(
                    content={
                        'body': result_dict
                    }
                )
            except Exception as err:
                return JSONResponse(
                    status_code= 500,
                    content={
                      "details": str(err) + " . Operation is unavailable.",  
                    }
                )
        else:
            try: 
                query = text(
                    """
                    SELECT *
                    FROM users
                    LIMIT :limit
                    OFFSET :offset;
                """)
                result = session.execute(query, {
                    "limit": limit,
                    "offset": offset}).mappings().all()
                result_dict = CursorResultDict(result)
                return JSONResponse(
                    content={
                        'body': result_dict
                    }
                )
            except Exception as err:
                return JSONResponse(
                    status_code= 500,
                    content={
                      "details": str(err) + " . Operation is unavailable.",  
                    }
                )
