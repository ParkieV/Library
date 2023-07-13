from fastapi import APIRouter
from app.routes import user 
from app.routes import book
from app.routes import librarian 
from app.routes import book_query 


api_router = APIRouter(prefix="/api")

api_router.include_router(book.routes, tags=["books"])
api_router.include_router(user.user_db_routes, tags=["users"])
api_router.include_router(user.user_routes, tags=["user"])
api_router.include_router(book_query.routes, tags=["queries"])
api_router.include_router(librarian.routes, tags=["librarian"])