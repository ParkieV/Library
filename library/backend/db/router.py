import json
from fastapi import APIRouter, Path
from typing import Annotated
from fastapi.responses import JSONResponse

from backend.db.schema import BookModel, BookGetDeleteModel, AuthModel, BookCreateUpdateModel
from backend.db.backends import BookMethods, UserMethods
from backend.db.models import Books as BookDB
from backend.db.models import Users as UserDB
from backend.db.schema import UserModel


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
        auth = AuthModel(
            email=body.email,
            password=body.password
        )
        auth_result = UserMethods.get_user_by_email_password(auth)
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
        auth = AuthModel(
            email=body.email,
            password=body.password
        )
        responce = UserMethods.get_user_by_email_password(auth)
        if responce.status_code == 200:
            user = json.loads(responce.body.decode('utf-8'))["user"]
            if user["user_type"] == 'Librarian' or user["user_type"] == 'Admin':
                if BookMethods.get_book_by_id(book_id).status_code == 200:
                    book = BookDB(
                        id=book_id,
                        title=body.title,
                        authors=body.authors,
                        user_id_taken=body.user_id_taken,
                        user_reserved_id=body.user_reserved_id,
                        date_start_use=body.date_start_use,
                        date_finish_use=body.date_finish_use
                    )
                    return BookMethods.update_book(book)
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
        auth = AuthModel(
            email=body.email,
            password=body.password
        )
        auth_result = UserMethods.get_user_by_email_password(auth)
        if auth_result.status_code != 200:
            return auth_result
        book = BookDB(
            title=body.title,
            authors=body.authors
        )
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
        auth = AuthModel(
            email=body.email,
            password=body.password
        )
        auth_result = UserMethods.get_user_by_email_password(auth)
        if auth_result.status_code != 200:
            return auth_result
        return BookMethods.delete_book_by_id(book_id)


class UsersDBViews():

    user_router = APIRouter(prefix="/users")

    @user_router.get("/action")
    def get_user(
        user_id: int = 0,
        body: 
        )
