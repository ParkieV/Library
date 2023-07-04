import json

from sqlalchemy import text
from pydantic import EmailStr

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from backend.schemas.users_schemas import UserDBModel
from backend.schemas.tokens_schemas import AuthModel
from backend.models.users import Users
from backend.db.serializer import CursorResultDict, json_serial


class UserMethods():
    def get_user_by_email(email: EmailStr, session: Session, *args, **kwargs) -> JSONResponse:
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
    
    def create_user(model: Users, session: Session, *args, **kwargs) -> JSONResponse:
        try:
            session.add(model)
            session.commit()
            session.close()
        except Exception as err:
            print(str(err))
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

    def get_user_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
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

    def update_user(model: UserDBModel, session: Session, *args, **kwargs) -> JSONResponse:
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

    def delete_user_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
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

    def get_user_by_email_password(model: AuthModel, session: Session, *args, **kwargs) -> JSONResponse:
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

    def get_database(session: Session, offset: int = 0, limit: int = 15, *args, **kwargs) ->JSONResponse:
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
