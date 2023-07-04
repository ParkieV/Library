
from sqlalchemy import text

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from backend.db.serializer import CursorResultDict
from backend.models.bookQuery import BookQuery


class BookQueryMethods():

    def get_bookQuery_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
        query = text("""
            SELECT *
            FROM book_queries
            WHERE id = :id
        """)
        try:
            result = session.execute(query, {"id": id}).mappings().first()
            return JSONResponse(
                content={
                    "query": CursorResultDict(result)
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable"
                }
            )

    def get_bookQuery_by_user_book(user_id: int, book_id: int, session: Session, *args, **kwargs) -> JSONResponse:
        query = text("""
            SELECT *
            FROM book_queries
            WHERE user_id = :user_id 
            AND book_id = :book_id
        """)
        try:
            result = session.execute(query, {"user_id": user_id, "book_id": book_id}).mappings().first()
            return JSONResponse(
                content={
                    "query": CursorResultDict(result)
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable"
                }
            )

    def create_bookQuery(model: BookQuery, session: Session, *args, **kwargs) -> JSONResponse:
        try:
            session.add(model)
        except Exception as err:
            return JSONResponse(
                status_code = 500,
                content={
                  "details": str(err) + ". Operation is unavailable.",  
                }
            )
        return JSONResponse(
            content={
                "details": 'OK'
            }
        )

    def delete_bookQuery_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
        query = BookQueryMethods.get_bookQuery_by_id(id)
        if query.status_code != 200:
            return query
        try:
            query = text("""
                DELETE FROM book_queries
                WHERE id = :id;
            """)
            session.execute(query, {
                "id": id
            })
            return JSONResponse(
                content={
                    "details": 'OK'
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code = 500,
                content={
                    "details": err + " . Operation is unavailable."
                }
            )
