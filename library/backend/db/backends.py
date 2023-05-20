import json

from sqlalchemy import create_engine, text, CursorResult
from pydantic import EmailStr
from typing import List, Annotated
from datetime import datetime, timedelta
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


class PasswordJWT():

    settings = JWTSettings()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(plain_password, hashed_password):
        return PasswordJWT.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return PasswordJWT.pwd_context.hash(password)
    
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, PasswordJWT.settings.secret_key, algorithm=PasswordJWT.settings.algorithm)
        return encoded_jwt

    def check_access_token(auth_model: TokenData, *args, **kwargs):
        user = UserMethods.get_user_by_email(auth_model.email)
        if user.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={"details": "User not found"}
            )
        user = UserDBModel.parse_obj(json.loads(user.body.decode["utf-8"])["user"])
        if auth_model.access_token == user.access_token:
            if datetime.today() - user.time_token_create > timedelta(minutes=JWTSettings.token_expire_minutes):
                user.access_token = None
                user.time_token_create = None
                UserMethods.update_user(user)
                return JSONResponse(
                    status_code=403,
                    content={"details": "Token is outdated"}
                )
            new_token = PasswordJWT.create_access_token({"sub": auth_model.email}, JWTSettings.token_expire_minutes)
            return JSONResponse(
                content={"token": new_token})
        return JSONResponse(
            status_code=403,
            content={"details": "Invalid token"}
        )


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
        if result:
            return JSONResponse(
                status_code = 200,
                content={
                    "user": CursorResultDict(result)
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
        if result:
            return JSONResponse(
                content={
                        "user": CursorResultDict(result)
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
            print(model)
            query = text("""
                UPDATE users
                SET (name, surname, email, user_type, access_token, time_token_create, hashed_password) = 
                (:name, :surname, :email, :user_type, :access_token, :time_token_create, :hashed_password)
                WHERE id = :id;
            """)
            session.execute(query, {
                "name": model.name,
                "surname": model.surname,
                #"last_name": model.last_name,
                "email": model.email,
                "user_type": model.user_type,
                #"book_id_taken": model.book_id_taken,
                #"reserved_book_id": model.reserved_book_id,
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
                UPDATE users
                SET (disabled)
                VALUES (TRUE)
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
                "details": 'Book not found'
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
        session = session["kwargs"]
        query = text("""
            SELECT *
            FROM bookQuery
            WHERE id = :id
        """)
        try:
            result = session.execute(query, {"id": id}).mapping().first()
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
    def get_bookQuery_by_id_user(user_id: int, *args, **kwargs) -> JSONResponse:
        session = session["kwargs"]
        query = text("""
            SELECT *
            FROM bookQuery
            WHERE user_id = :user_id
        """)
        try:
            result = session.execute(query, {"user_id": user_id}).mapping().first()
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
        session = session["kwargs"]
        query = BookMethods.get_book_by_id(id)
        if query.status_code != 200:
            return query
        try:
            query = text("""
                DELETE FROM bookQueries
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
