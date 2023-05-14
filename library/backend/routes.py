from fastapi import APIRouter, Path
from typing import Annotated
from fastapi.responses import JSONResponse

from backend.db.router import BooksDBViews
from backend.db.backends import BookMethods


router = APIRouter(prefix="/api")


@router.get("/search/{book_title}")
async def search_book(
        book_title: Annotated[str, Path(title="Book title for search")]
) -> JSONResponse:
    return BookMethods.search_book_by_title(book_title)


router.include_router(BooksDBViews.book_router, tags=["books"])