from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.books import BookModel, BookDBModel

from app.crud import books

from app.core.db_conn import get_async_session


routes = APIRouter(prefix="/books")


@routes.get("/action", response_model=BookDBModel)
async def get_book(book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    return await books.get_book_by_id(session, book_id)


@routes.post("/action", response_model=BookDBModel)
async def update_book(body: BookModel, book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    current_schema = BookDBModel(id=book_id,
                                 name=body.name,
                                 authors=body.authors,
                                 user_id_taken=body.user_id_taken,
                                 user_reserved_id=body.user_reserved_id,
                                 date_start_reserve=body.date_start_reserve,
                                 date_start_use=body.date_finish_use,
                                 date_finish_use=body.date_finish_use)

    return await books.update_book(session, current_schema)


@routes.put("/action", response_model=BookModel)
async def create_book(body: BookModel, session: AsyncSession = Depends(get_async_session)):
    return await books.create_book(session, body)


@routes.delete("/action", response_model=BookDBModel)
async def delete_book(book_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    return await books.delete_book_by_id(session, book_id)
