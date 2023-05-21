import json

from pydantic import EmailStr
from datetime import timedelta, datetime
from sqlalchemy import func

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from backend.db.backends import UserMethods, BookMethods, BookQueryMethods, PasswordJWT
from backend.db.schema import BookQueryModel, UserDBModel
from backend.db.models import Users, Books
from backend.db.settings import JWTSettings


def reserve_book(user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if user["reserved_book_id"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "User has reserved a book"
            }
        )
    if book["user_reserved_id"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Book has been reserved already"
            }
        )
    query = BookQueryModel(
        user_id=user["id"],
        book_id=book["id"],
        type_order="Add",
        type_query="Reserve"
    )
    BookQueryMethods.create_bookQuery(query)

def cancel_reserve_book(user_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(user["reserved_book_id"]).body.encode['utf-8'])["book"]
    query = json.loads(BookQueryMethods.get_bookQuery_by_id_user(user_id).body.encode['utf-8'])["query"]
    try:
        changed_user = Users(
            id=user["id"],
            name=user["name"],
            surname=user["surname"],
            last_name=user["last_name"],
            email=user["email"],
            password=user["password"],
            user_type=user["user_type"],
            book_id_taken=user["book_id_taken"],
            reserved_book_id=None
        )
        UserMethods.update_user(changed_user)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    try:
        changed_book = Books(
            id=book["id"],
            title=book["title"],
            authors=book["authors"],
            user_reserved_id=None,
            date_start_reserve=None,
            date_start_use=book["date_start_use"],
            date_finish_use=book["date_finish_use"],
            )
        BookMethods.update_book(changed_book)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    return BookQueryMethods.delete_bookQuery_by_id(query["id"])

def take_book(user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if user["book_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "User has taken a book"
            }
        )
    if book["user_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Book has been taken already"
            }
        )
    query = BookQueryModel(
        user_id=user["id"],
        book_id=book["id"],
        type_order="Add",
        type_query="Take"

    )
    BookQueryMethods.create_bookQuery(query)

def cancel_take_book(user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if not user["book_id_taken"] or not book["user_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
    query = BookQueryModel(
        user_id=user["id"],
        book_id=book["id"],
        type_order="Cancel",
        type_query="Take"

    )
    BookQueryMethods.create_bookQuery(query)

def authenticate_user(email: EmailStr, password: str, id: int):
    user = UserMethods.get_user_by_email(email)
    if user.status_code != 200:
        return user
    user = UserDBModel.parse_obj(json.loads(user.body.decode("utf-8"))["user"])
    if user.id != id:
        return JSONResponse(
            status_code=400,
            content={"details": "User params is uncorrect"}
        )
    if not PasswordJWT.verify_password(password, user.hashed_password):
        return JSONResponse(
            status_code=400,
            content={
                "details": "Uncorrect password"
            }
        )
    jwt_settings = JWTSettings()
    access_token_expires = timedelta(minutes=int(jwt_settings.token_expire_minutes))
    user.access_token = PasswordJWT.create_access_token({"sub": user.email}, access_token_expires)
    user.time_token_create = datetime.now().isoformat()
    UserMethods.update_user(user)
    return JSONResponse(
        content={
            "user": user.dict()
        }
    )
    