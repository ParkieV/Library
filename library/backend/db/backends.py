import re
import json

from sqlalchemy import create_engine, update, text, CursorResult
from pydantic import EmailStr
from fastapi import status
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.declarative import DeclarativeMeta

from backend.db.schema import UserModel, BookModel, BookCreateUpdateModel, AuthModel
from backend.db.models import Users, Books
from backend.db.settings import DBSettings


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
    
    @staticmethod
    def _email_validation(email: EmailStr) -> bool:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(email_regex, email)
    
    @staticmethod
    def _auth_validation(email: EmailStr, password: str) -> bool:
        if not UserMethods._email_validation(email):
            print("Invalid email")
            return False
        return True
    
    @setUp
    def get_user_by_email(email: EmailStr, *args, **kwargs) -> UserModel | None:
        session = kwargs["session"]
        if not UserMethods._email_validation(email):
            return {
                'status': 500,
                "details": 'Invalid email.'
            }
        result = session.query(Users).filter(Users.email == email).first()
        if result:
            return {
                'status': 200,
                "details": 'OK',
                'body': result
            }
        return {
            'status': 500,
            "details": 'User not found.',
            'body': None
        }
    
    @setUp
    def create_user(model: UserModel, *args, **kwargs) -> dict:
        session = kwargs["session"]
        if not UserMethods._auth_validation(model.email, model.password):
            return {
                'status': 500,
                "details": 'Invalid email or password.'
            }
        if UserMethods.get_user_by_email(model.email)['status'] != 500:
            return {
                'status': 500,
                "details": 'User already exists.'
            }
        try:
            session.add(model)
        except Exception as err:
            return {
                'status': 500,
                "details": err + " . Operation is unavailable."
            }
        return {
            'status': 200,
            "details": 'OK'
        }

    @setUp
    def get_user_by_id(id: int, *args, **kwargs) -> UserModel | None:
        session = kwargs["session"]
        result = session.query(Users).filter(Users.id == id).first()
        if result:
            return {
                'status': 200,
                "details": 'OK',
                'body': result
            }
        return {
            'status': 500,
            "details": 'User not found.',
            'body': None
        }

    @setUp
    def update_user(model: UserModel, *args, **kwargs) -> dict:
        session = kwargs["session"]
        user = UserMethods.get_user_by_id(model.id)
        if user['status'] != 200:
            return user
        try:
            stmt = (
                update(Users).
                where(Users.id == model.id).
                values(model.dict(exclude_unset=True)).
                returning(Users)
            )
            result = session.execute(stmt)
            return {
                'status': 200,
                "details": 'OK',
                'body': result
            }
        except Exception as err:
            return {
                'status': 500,
                "details": err + " . Operation is unavailable.",
                'body': None
            }

    @setUp
    def delete_user_by_id(id: int, *args, **kwargs) -> dict:
        session = kwargs["session"]
        user = UserMethods.get_user_by_id(id)
        if user['status'] != 200:
            return user
        try:
            request = Users.query.filter(Users.id == id).first()
            session.delete(request)
            return {
                'status': 200,
                "details": 'OK',
            }
        except Exception as err:
            return {
                'status': 500,
                "details": err + " . Operation is unavailable."
            }
    
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
                WHERE title LIKE :new_title;
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
    
    @setUp
    def get_book_by_title_authors(title: str, authors: str, *args, **kwargs) -> dict:
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
    def get_book_by_id(id: int, *args, **kwargs) -> dict:
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
                "details": 'Book not found'
                }
            )

    @setUp
    def delete_book_by_id(id: int, *args, **kwargs):
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
    def update_book(model: Books, *args, **kwargs) -> dict:
        session = kwargs["session"]
        try:
            print(model)
            query = text("""
                UPDATE books
                SET (title, authors, user_id_taken, user_reserved_id, date_start_use, date_finish_use) = 
                (:title, :authors, :user_id_taken, :user_reserved_id, :date_start_use, :date_finish_use) 
                WHERE id = :id;
            """)
            session.execute(query, {
                "title": model.title,
                "authors": model.authors,
                "user_id_taken": model.user_id_taken,
                "user_reserved_id": model.user_reserved_id,
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

def CursorResultDict(obj: CursorResult | List[CursorResult], *args, **kwargs) -> dict:
            if type(obj) is list:
                result_keys, result_items = [elem.keys() for elem in obj], [elem.items() for elem in obj]
                result_dict = []
                for i in range(len(result_keys)):
                    result_dict.append(dict(zip(result_keys[i], result_items[i])))
                for i in range(len(result_dict)):
                    for key in result_dict[i].keys():
                        result_dict[i][key] = result_dict[i][key][1:]
                        if len(result_dict[i][key]) == 1:
                            result_dict[i][key] = result_dict[i][key][0]
            else:
                result_keys, result_items = obj.keys(), obj.items()
                result_dict = dict(zip(result_keys, result_items))
                for key in result_dict.keys():
                    result_dict[key] = result_dict[key][1:]
                    if len(result_dict[key]) == 1:
                        result_dict[key] = result_dict[key][0]
            return result_dict
