from fastapi import APIRouter

from app.routes import book, book_query, librarian, tokens, user

api_router = APIRouter(prefix="/api")

api_router.include_router(book.routes, tags=["books"])
api_router.include_router(user.user_db_routes, tags=["users"])
api_router.include_router(user.user_routes, tags=["user"])
api_router.include_router(book_query.routes, tags=["queries"])
api_router.include_router(librarian.routes, tags=["librarian"])
api_router.include_router(tokens.routes, tags=["tokens"])
