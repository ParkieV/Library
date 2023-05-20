import json

from datetime import datetime

from fastapi.responses import JSONResponse

from backend.db.backends import UserMethods, BookMethods, BookQueryMethods
from backend.db.models import Books, Users


def accept_reserve_book(user_id: int, book_id: int) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if not user["reserved_book_id"] or not book["user_reserved_id"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
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
            reserved_book_id=book_id
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
            user_reserved_id=user_id,
            date_start_reserve=datetime.today().strftime("%d.%m.%Y"),
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

def accept_take_book(user_id: int, book_id: int, date_finish: datetime.date) -> JSONResponse:
    user = json.loads(UserMethods.get_user_by_id(user_id).body.encode['utf-8'])["user"]
    book = json.loads(BookMethods.get_book_by_id(book_id).body.encode['utf-8'])["book"]
    if not user["book_id_taken"] or not book["user_id_taken"]:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
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
            book_id_taken=user_id,
            reserved_book_id=user["reserved_book_id"]
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
            user_reserved_id=user["user_reserved_id"],
            date_start_reserve=user["date_start_reserve"],
            date_start_use=datetime.today().strftime("%d.%m.%Y"),
            date_finish_use=date_finish,
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
            book_id_taken=None,
            reserved_book_id=user["reserved_book_id"]
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
            user_reserved_id=user["user_reserved_id"],
            date_start_reserve=user["date_start_reserve"],
            date_start_use=None,
            date_finish_use=None,
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
