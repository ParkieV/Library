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


class BookQueryMethods():
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
    def get_bookQuery_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        query = text("""
            SELECT *
            FROM book_queries
            WHERE id = :id
        """)
        try:
            result = session.execute(query, {"id": id}).mappings().first()
            return JSONResponse(
                content={
                    "query": CursorResultDict(result)
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable"
                }
            )

    @setUp
    def get_bookQuery_by_user_book(user_id: int, book_id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        query = text("""
            SELECT *
            FROM book_queries
            WHERE user_id = :user_id 
            AND book_id = :book_id
        """)
        try:
            result = session.execute(query, {"user_id": user_id, "book_id": book_id}).mappings().first()
            return JSONResponse(
                content={
                    "query": CursorResultDict(result)
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable"
                }
            )

    @setUp
    def create_bookQuery(model: BookQuery, *args, **kwargs) -> JSONResponse:
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
    def delete_bookQuery_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        query = BookQueryMethods.get_bookQuery_by_id(id)
        if query.status_code != 200:
            return query
        try:
            query = text("""
                DELETE FROM book_queries
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
                    "details": err + " . Operation is unavailable."
                }
            )
