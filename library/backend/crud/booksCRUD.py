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


class BookMethods():
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
    def search_book_by_title(book_title: str, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        try: 
            query = text(
                """
                SELECT b.id, b.title, b.authors
                FROM books as b 
                WHERE title 
                LIKE :new_title;
            """)
            result = session.execute(query, {"new_title": "%" + book_title + "%"}).mappings().all()
            result_dict = CursorResultDict(result)
            if result_dict == []:
                return JSONResponse(
                    status_code = 404,
                    content={
                        "details": 'Book not found'
                    }
                    
                )
            return JSONResponse(
                content={
                    "books": result_dict
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code= 500,
                content={
                  "details": str(err) + " . Operation is unavailable.",  
                }
            )
    
    @setUp
    def get_book_by_title_authors(title: str, authors: str, *args, **kwargs) -> JSONResponse:
        session = kwargs['session']
        query = text("""
            SELECT *
            FROM books
            WHERE id = :book_title
            AND author;
        """)
        result = session.execute(query, {"book_id": id}).mappings().first()
        if result:
            return JSONResponse(
                content={
                        "book": CursorResultDict(result)
                }
            )
        else:
            return JSONResponse(
                status_code = 404,
                content = {
                "details": 'Book not found'
                }
            )

    @setUp
    def create_book(model: Books, *args, **kwargs) -> JSONResponse:
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
    def get_book_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs['session']
        query = text("""
            SELECT *
            FROM books
            WHERE id = :book_id;
        """)
        result = session.execute(query, {"book_id": id}).mappings().first()
        if result:
            return JSONResponse(
                content={
                        "book": CursorResultDict(result)
                }
            )
        else:
            return JSONResponse(
                status_code = 404,
                content = {
                "details": 'Book not found7'
                }
            )

    @setUp
    def delete_book_by_id(id: int, *args, **kwargs) -> JSONResponse:
        session = kwargs['session']
        book = BookMethods.get_book_by_id(id)
        if book.status_code != 200:
            return book
        try:
            query = text("""
                DELETE FROM books
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

    @setUp
    def update_book(model: BookDBModel, *args, **kwargs) -> JSONResponse:
        session = kwargs["session"]
        try:
            print(model)
            query = text("""
                UPDATE books
                SET (title, authors, user_id_taken, user_reserved_id, date_start_reserve, date_start_use, date_finish_use) = 
                (:title, :authors, :user_id_taken, :user_reserved_id, :date_start_reserve, :date_start_use, :date_finish_use) 
                WHERE id = :id;
            """)
            session.execute(query, {
                "title": model.title,
                "authors": model.authors,
                "user_id_taken": model.user_id_taken,
                "user_reserved_id": model.user_reserved_id,
                "date_start_reserve": model.date_start_reserve,
                "date_start_use": model.date_start_use,
                "date_finish_use": model.date_finish_use,
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
    def get_database(offset: int = 0, limit: int = 15, *args, **kwargs) ->JSONResponse:
        session = kwargs["session"]
        if limit == 0:
            try: 
                query = text(
                    """
                    SELECT *
                    FROM books;
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
                    FROM books
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
