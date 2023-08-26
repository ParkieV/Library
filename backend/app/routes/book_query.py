from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.crud import book_query
from app.schemas.book_query import BookQueryDBModel, BookQueryModel

routes = APIRouter(prefix="/queries")


@routes.get("/action", response_model=BookQueryDBModel)
async def get_query(query_id: int = 0, session: AsyncSession = Depends(get_async_session)):
	return await book_query.get_book_query_by_id(session, query_id)


@routes.put("/action", response_model=BookQueryModel)
async def create_query(body: BookQueryModel, session: AsyncSession = Depends(get_async_session)):
	return await book_query.create_book_query(session, body)


@routes.delete("/action", response_model=BookQueryDBModel)
async def delete_query(query_id: int, session: AsyncSession = Depends(get_async_session)):
	return await book_query.delete_book_query_by_id(session, query_id)
