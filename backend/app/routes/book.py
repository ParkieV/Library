from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.crud import books
from app.schemas.books import BookDBModel

routes = APIRouter(prefix="/books")


@routes.get("/action", response_model=BookDBModel)
async def get_book(book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
	return await books.get_book_by_id(session, book_id)


@routes.get("/get_books", response_model=List[BookDBModel] | None)
async def get_books_view(page: int, limit: int = 15, session: AsyncSession = Depends(get_async_session)) -> List[BookDBModel] | None:

	result = await books.get_books(session, (page - 1)*15, limit)
	return result
