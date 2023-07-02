import json
from fastapi import APIRouter, Path
from typing import Annotated
from datetime import datetime
from fastapi.responses import JSONResponse

from backend.db.schema import BookGetDeleteModel, BookCreateUpdateModel, UserDBModel, UserHashedModel
from backend.db.backends import BookMethods, UserMethods, BookQueryMethods, PasswordJWT
from backend.db.schema import BookQueryModel, QueryGetDeleteModel, QueryCreateModel
from backend.db.models import Books as BookDB
from backend.db.models import Users as UserDB
from backend.db.schema import UserGetDeleteModel, UserCreateUpdateModel
from backend.user.schema import UserAuthModel


class BooksViews():

    books_router = APIRouter(prefix="/books")

    @books_router.get("/action")
    def get_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_book = BookMethods.get_book_by_id(book_id)
                response_book = json.loads(response_book.body.decode('utf-8'))
                response_book["access_token"] = token
                return JSONResponse(
                    content=response_book
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )

    @books_router.post("/action")
    def update_book(
        book_id : int = 0,
        body: BookCreateUpdateModel = None) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == 'Librarian':
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                if BookMethods.get_book_by_id(book_id).status_code == 200:
                    book_db = BookDB(**body.book.dict())
                    book_db.id = book_id
                    response_book = BookMethods.update_book(book_db)
                    response_book = json.loads(response_book.body.decode('utf-8'))
                    response_book["access_token"] = token
                    return JSONResponse(
                        content=response_book
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "details": "Uncorrect request"
                        }
                    )
            else:
                return JSONResponse(
                    status_code=403,
                    content = {
                        "details": "Access denied"
                    }
                )

    @books_router.put("/action")
    def create_book(body: BookCreateUpdateModel) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                book = BookDB(**body.book.dict())
                response_book = BookMethods.create_book(book)
                response_book = json.loads(response_book.body.decode('utf-8'))
                response_book["access_token"] = token
                return JSONResponse(
                    content=response_book
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )

    @books_router.delete("/action")
    def delete_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_book = BookMethods.delete_book_by_id(book_id)
                response_book = json.loads(response_book.body.decode('utf-8'))
                response_book["access_token"] = token
                return JSONResponse(
                    content=response_book
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )
