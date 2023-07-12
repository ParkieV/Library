from fastapi import APIRouter
from app.routes.user import UsersDBViews, UserViews
from app.routes import book
from app.routes import librarian 
from app.routes import book_query 


api_router = APIRouter(prefix="/api")

api_router.include_router(book.routes, tags=["books"])
api_router.include_router(UsersDBViews.user_db_routes, tags=["users"])
api_router.include_router(UserViews.user_routes, tags=["user"])
api_router.include_router(book_query.routes, tags=["queries"])
api_router.include_router(librarian.routes, tags=["librarian"])