from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.crud import books, users
from app.methods.librarian import (
	accept_reserve_book,
	accept_take_book,
	cancel_take_book,
)
from app.methods.tokens import checkAccess
from app.schemas.book_query import BookQueryDBModel, UserQueryActionModel
from app.schemas.books import BookDBModel, BookModel

routes = APIRouter(prefix="/librarian")


@routes.post("/accept_reserve", response_model=BookQueryDBModel)
async def accept_reserve_query(body: UserQueryActionModel, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	user = await users.get_user_by_id(session, body.user_id)
	match user:
		case user if user.user_type != "Librarian":
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian.")

	return await accept_reserve_book(body.email, body.user_id, body.book_id, session)


@routes.post("/accept_take", response_model=BookQueryDBModel)
async def accept_take_query(body: UserQueryActionModel, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	user = await users.get_user_by_id(session, body.user_id)
	match user:
		case user if user.user_type != "Librarian":
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian")

	return await accept_take_book(body.email, body.user_id, body.book_id, session)


@routes.post("/cancel_take", response_model=BookQueryDBModel)
async def cancel_take_query(body: UserQueryActionModel, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	user = await users.get_user_by_id(session, body.user_id)
	match user:
		case user if user.user_type != "Librarian":
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a librarian")

	return await cancel_take_book(body.email, body.user_id, body.book_id, session)


@routes.post("/book", response_model=BookDBModel)
async def update_book(body: BookModel, book_id: int = 0, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	current_schema = BookDBModel(bookId=book_id, **body.dict())

	return await books.update_book(session, current_schema)


@routes.put("/book", response_model=BookModel)
async def create_book(body: BookModel, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	return await books.create_book(session, body)


@routes.delete("/book", response_model=BookDBModel)
async def delete_book(book_id: int = 0, check_access: None = Depends(checkAccess),
			session: AsyncSession = Depends(get_async_session)):

	if check_access != "Librarian":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

	return await books.delete_book_by_id(session, book_id)
