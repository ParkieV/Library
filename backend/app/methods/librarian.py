from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import book_query, books, users
from app.schemas.book_query import BookQueryDBModel


async def accept_reserve_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel:

	if (user := await users.get_user_by_id(session, user_id)).reserved_book_id:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="User has reserved a book")
	if (book := await books.get_books_by_id(session, user.reserved_book_id)) != book_id:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="Book id is uncorrect")
	if book.user_reserved_id:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Book had been reserved")

	query = book_query.get_book_query_by_user_book_id(
		session, user.id, book.id)

	user.reserved_book_id = book_id
	book.user_reserved_id = user_id

	await users.update_user(session, user)
	await books.create_book(session, book)

	return await book_query.delete_book_query_by_id(session, query.id)


async def accept_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession,
						   date_finish=datetime.now(timezone.utc) + timedelta(days=31)) -> BookQueryDBModel:

	if (user := await users.get_user_by_id(session, user_id)).book_id_taken:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="User has taken a book")
	if (book := await books.get_books_by_id(session, user.reserved_book_id)) != book_id:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="Book id is uncorrect")
	if book.user_id_taken:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Book had been taken")

	query = book_query.get_book_query_by_user_book_id(
		session, user.id, book.id)

	user.book_id_taken = book_id
	book.user_id_taken = user_id
	book.date_start_use = datetime.now()
	book.date_finish_use = date_finish

	await users.update_user(session, user)
	await books.create_book(session, book)

	return await book_query.delete_book_query_by_id(session, query.id)


async def cancel_take_book(email: EmailStr, user_id: int, book_id: int, session: AsyncSession) -> BookQueryDBModel:

	if not (user := await users.get_user_by_id(session, user_id)).book_id_taken:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="User hasn't take book.")
	if (book := await books.get_books_by_id(session, user.reserved_book_id)) != book_id:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST, detail="Book id is uncorrect")
	if not book.user_id_taken:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Book hadn't taken by user.")

		query = book_query.get_book_query_by_user_book_id(
			session, user.id, book.id)

		user.book_id_taken = None
		book.user_id_taken = None
		book.date_start_use = None
		book.date_finish_use = None

		await users.update_user(session, user)
		await books.create_book(session, book)

		return await book_query.delete_book_query_by_id(session, query.id)
