from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.book_query import BookQueryDBModel, BookQueryModel

from app.crud.book_query import BookQueryMethods

from app.core.db_conn import get_async_session

from app.methods.error_handler import sql_validation_error

routes = APIRouter(prefix="/queries")


@routes.get("/action", response_model=BookQueryDBModel)
async def get_query(query_id: int = 0, session: AsyncSession = Depends(get_async_session)):
    return await BookQueryMethods.get_book_query_by_id(session, query_id)


@routes.put("/action", response_model=BookQueryModel)
async def create_query(body: BookQueryModel, session: AsyncSession = Depends(get_async_session)):
    return await BookQueryMethods.create_book_query(session, body)


@routes.delete("/action", response_model=BookQueryDBModel)
async def delete_query(query_id: int, session: AsyncSession = Depends(get_async_session)):
    return await BookQueryMethods.delete_book_query_by_id(session, query_id)
