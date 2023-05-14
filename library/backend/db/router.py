import json
from fastapi import APIRouter, Path, status
from typing import Annotated
from fastapi.responses import JSONResponse

from backend.db.schema import Book, BookGetDelete, ModelAuth, BookUpdate
from backend.db.backends import BookMethods, UserMethods

from backend.db.schema import User


class BooksDBViews():

    book_router = APIRouter(prefix="/books")

    @book_router.get("/{book_id}")
    def get_book(
        book_id : Annotated[int, Path(title="The ID of the book to get")],
        body: BookGetDelete
    ) -> JSONResponse:
        auth = ModelAuth(
            email=body.email,
            password=body.password
        )
        auth_result = UserMethods.get_user_by_email_password(auth)
        if auth_result.status_code != 200:
            return auth_result
        return BookMethods.get_book_by_id(book_id)
    
    @book_router.post("/{book_id}")
    def update_book(
        book_id : Annotated[int, Path(title="The ID of the book to get")],
        body: BookUpdate
    ) -> JSONResponse:
        auth = ModelAuth(
            email=body.email,
            password=body.password
        )
        responce = UserMethods.get_user_by_email_password(auth)
        if responce.status_code == 200:
            user = responce.content.body
            if user.user_type == 'Librarian':
                if body.id == book_id:
                    book = Book(
                        id=body.id,
                        title=body.title,
                        authors=body.authors,
                        user_id_taken=body.user_id_taken,
                        user_reserved_id=body.user_reserved_id,
                        date_start_use=body.date_start_use,
                        date_finish_use=body.date_finish_use
                    )
                    BookMethods.update_book(book)
                else:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content=json.loads({
                            "message": "Uncorrect request"
                        })
                    )
            else:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content = json.loads({
                        'message': 'Access denied'
                    })
                )
        else:
            return responce

