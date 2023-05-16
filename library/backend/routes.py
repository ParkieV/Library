from fastapi import APIRouter, Path
from typing import Annotated
from fastapi.responses import JSONResponse

from backend.db.router import BooksDBViews, UsersDBViews
from backend.db.backends import BookMethods


router = APIRouter(prefix="/api")


@router.get("/search")
async def search_book(text: str = "") -> JSONResponse:
    if text == "":
        return JSONResponse(
            status_code=400,
            content={
                "details": "Uncorrect request."
            }
        )
    print(text)
    return BookMethods.search_book_by_title(text)


router.include_router(BooksDBViews.book_router, tags=["books"])
router.include_router(UsersDBViews.user_router, tags=["users"])