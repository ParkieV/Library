import json

from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from fastapi.responses import JSONResponse

from backend.crud.usersCRUD import UserMethods
from backend.crud.booksCRUD import BookMethods
from backend.crud.bookQueryCRUD import BookQueryMethods
from backend.schemas.users_schemas import UserDBModel
from backend.schemas.books_schemas import BookDBModel
from backend.models.users import Users
from backend.models.books import Books


def accept_reserve_book(email: EmailStr, user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_email(email).body.decode('utf-8'))["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.decode('utf-8'))["book"]
    if user["reserved_book_id"] or book["user_reserved_id"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
    query = json.loads(BookQueryMethods.get_bookQuery_by_user_book(user_id, book_id).body.decode('utf-8'))["query"]
    try:
        changed_user = UserDBModel.parse_obj(user)
        changed_user.reserved_book_id = book_id
        changed_user = Users(**changed_user.dict())
        UserMethods.update_user(changed_user)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    try:
        changed_book = BookDBModel.parse_obj(book)
        changed_book.user_reserved_id = user_id
        changed_book.date_start_reserve = datetime.now().isoformat()
        changed_book = Books(**changed_book.dict())
        BookMethods.update_book(changed_book)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    return BookQueryMethods.delete_bookQuery_by_id(query["id"])

def accept_take_book(email: EmailStr, user_id: int, book_id: int, date_finish: datetime.now(timezone.utc) + timedelta(days=31)) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_email(email).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if user["book_id_taken"] or book["user_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
    query = json.loads(BookQueryMethods.get_bookQuery_by_user_book(user_id, book_id).body.encode['utf-8'])["query"]
    try:
        changed_user = UserDBModel.parse_obj(user)
        changed_user.book_id_taken = book_id
        changed_user = Users(**changed_user.dict())
        UserMethods.update_user(changed_user)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    try:
        changed_book = BookDBModel.parse_obj(book)
        changed_book.user_id_taken = user_id
        changed_book.date_start_use = datetime.now()
        changed_book.date_finish_use = date_finish
        changed_book = Books(**changed_book.dict())
        BookMethods.update_book(changed_book)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    return BookQueryMethods.delete_bookQuery_by_id(query["id"])

def cancel_take_book(email: EmailStr, user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_email(email).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if user["book_id_taken"] or book["user_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
    query = json.loads(BookQueryMethods.get_bookQuery_by_user_book(user_id, book_id).body.encode['utf-8'])["query"]
    try:
        changed_user = UserDBModel.parse_obj(user)
        changed_user.book_id_taken = None
        changed_user = Users(**changed_user.dict())
        UserMethods.update_user(changed_user)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    try:
        changed_book = BookDBModel.parse_obj(book)
        changed_book.user_id_taken = None
        changed_book.date_start_use = None
        changed_book.date_finish_use = None
        changed_book = Books(**changed_book.dict())
        BookMethods.update_book(changed_book)
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={
                "details": str(err) + ". Operation is unavailable"
            }
        )
    return BookQueryMethods.delete_bookQuery_by_id(query["id"])