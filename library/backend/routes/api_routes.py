from fastapi import APIRouter
from backend.routes.user_routes import UsersDBViews, UserViews
from backend.routes.book_routes import BooksDBViews
from backend.routes.book_query_routes import BookQueriesDBViews
from backend.routes.librarian_routes import LibrarianViews


api_router = APIRouter(prefix="/api")

api_router.include_router(BooksDBViews.books_router, tags=["books"])
api_router.include_router(UsersDBViews.users_router, tags=["users"])
api_router.include_router(UserViews.user_router, tags=["user"])
api_router.include_router(BookQueriesDBViews.queries_router, tags=["queries"])
api_router.include_router(LibrarianViews.librarian_router, tags=["librarian"])