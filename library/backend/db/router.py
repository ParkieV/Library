import json
from fastapi import APIRouter, Path
from typing import Annotated
from fastapi.responses import JSONResponse

from backend.db.schema import BookGetDeleteModel, AuthModel, BookCreateUpdateModel
from backend.db.backends import BookMethods, UserMethods
from backend.db.models import Books as BookDB
from backend.db.models import Users as UserDB
from backend.db.schema import UserGetDeleteModel, UserCreateUpdateModel


class BooksDBViews():

    book_router = APIRouter(prefix="/books")

    @book_router.get("/action")
    def get_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None
    ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,    
                content={
                    "details": "Uncorrect request."
                }
            )
        print(body)
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        return BookMethods.get_book_by_id(book_id)
    
    @book_router.post("/action")
    def update_book(
        book_id : int = 0,
        body: BookCreateUpdateModel = None
    ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        responce = UserMethods.get_user_by_email_password(body.auth)
        if responce.status_code == 200:
            user = json.loads(responce.body.decode('utf-8'))["user"]
            if user["user_type"] == 'Librarian' or user["user_type"] == 'Admin':
                if BookMethods.get_book_by_id(book_id).status_code == 200:
                    book_db = BookDB(**body.book.dict())
                    book_db.id = book_id
                    return BookMethods.update_book(book_db)
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "message": "Uncorrect request"
                        }
                    )
            else:
                return JSONResponse(
                    status_code=403,
                    content = {
                        'message': 'Access denied'
                    }
                )
        else:
            return responce

    @book_router.put("/create")
    def create_book(body: BookCreateUpdateModel) -> JSONResponse:
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        book = BookDB(**body.book.dict())
        return BookMethods.create_book(book)

    @book_router.delete("/action")
    def delete_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None
    ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        return BookMethods.delete_book_by_id(book_id)


class UsersDBViews():

    user_router = APIRouter(prefix="/users")

    @user_router.get("/action")
    def get_user(
        user_id: int = 0,
        body: UserGetDeleteModel = None
        ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        return UserMethods.get_user_by_id(user_id)
 
    @user_router.delete("/action")
    def delete_user(
        book_id: int = 0,
        body: BookGetDeleteModel = None
    ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        return UserMethods.delete_user_by_id(book_id)

    @user_router.put("/create")
    def create_user(body: UserCreateUpdateModel) -> JSONResponse:
        print(body)
        auth_result = UserMethods.get_user_by_email_password(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        user = UserDB(**body.user.dict())
        return UserMethods.create_user(user)

    @user_router.post("/action")
    def update_user(
        user_id : int = 0,
        body: UserCreateUpdateModel = None
    ) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        responce = UserMethods.get_user_by_email_password(body.auth)
        if responce.status_code == 200:
            user = json.loads(responce.body.decode('utf-8'))["user"]
            if user["user_type"] == 'Admin':
                if UserMethods.get_user_by_id(user_id).status_code == 200:
                    user = UserDB(**body.user.dict())
                    user.id = user_id
                    return UserMethods.update_user(user)
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "message": "Uncorrect request"
                        }
                    )
            else:
                return JSONResponse(
                    status_code=403,
                    content = {
                        'message': 'Access denied'
                    }
                )
        else:
            return responce
