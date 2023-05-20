import json

from fastapi import APIRouter, Path
from typing import List, Dict
from fastapi.responses import JSONResponse

from backend.db.router import BooksDBViews, UsersDBViews
from backend.db.backends import BookMethods, UserMethods
from backend.user.router import UserViews


router = APIRouter(prefix="/api")

@router.get("/search")
async def search_book(text: str = "") -> JSONResponse:
    books = BookMethods.search_book_by_title(text)
    books = json.loads(books.body.decode('utf-8'))["books"]
    return books

@router.get("/book_table")
async def get_books(page: int = 1,
                    limit: int = 15,
                    books: List[Dict] | None = None) -> JSONResponse:
    if not books:
        books = BookMethods.search_book_by_title("")
        books = json.loads(books.body.decode('utf-8'))["books"]
    if len(books) <= (page - 1) * limit:
        return JSONResponse(
            status_code = 400,
            content={
                "details": "Uncorrect params"
            }
        )
    else:
        return JSONResponse(
            content={
                "books": books[(page - 1) * limit: min(len(books), page * limit)]
            }
        )

@router.get("/user_table")
async def get_users(page: int = 1,
                    limit: int = 15) -> JSONResponse:
    return UserMethods.get_database(offset = (page - 1) * limit,
                                    limit = limit)
    

router.include_router(BooksDBViews.books_router, tags=["books"])
router.include_router(UsersDBViews.users_router, tags=["users"])
router.include_router(UserViews.user_router, tags=["user"])
