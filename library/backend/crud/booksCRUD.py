from sqlalchemy import text

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from backend.db.serializer import CursorResultDict
from backend.models.books import Books
from backend.schemas.books_schemas import BookDBModel


class BookMethods():
    
    def search_book_by_title(book_title: str, session: Session, *args, **kwargs) -> JSONResponse:
        try: 
            query = text(
                """
                SELECT b.id, b.title, b.authors
                FROM books as b 
                WHERE title 
                LIKE :new_title;
            """)
            result = session.execute(query, {"new_title": "%" + book_title + "%"}).mappings().all()
            result_dict = CursorResultDict(result)
            if result_dict == []:
                return JSONResponse(
                    status_code = 404,
                    content={
                        "details": 'Book not found'
                    }
                    
                )
            return JSONResponse(
                content={
                    "books": result_dict
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code= 500,
                content={
                  "details": str(err) + " . Operation is unavailable.",  
                }
            )
    
    def get_book_by_title_authors(title: str, authors: str, session: Session, *args, **kwargs) -> JSONResponse:
        query = text("""
            SELECT *
            FROM books
            WHERE id = :book_title
            AND author;
        """)
        result = session.execute(query, {"book_id": id}).mappings().first()
        if result:
            return JSONResponse(
                content={
                        "book": CursorResultDict(result)
                }
            )
        else:
            return JSONResponse(
                status_code = 404,
                content = {
                "details": 'Book not found'
                }
            )

    def create_book(model: Books, session: Session, *args, **kwargs) -> JSONResponse:
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

    def get_book_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
        query = text("""
            SELECT *
            FROM books
            WHERE id = :book_id;
        """)
        result = session.execute(query, {"book_id": id}).mappings().first()
        if result:
            return JSONResponse(
                content={
                        "book": CursorResultDict(result)
                }
            )
        else:
            return JSONResponse(
                status_code = 404,
                content = {
                "details": 'Book not found7'
                }
            )

    def delete_book_by_id(id: int, session: Session, *args, **kwargs) -> JSONResponse:
        book = BookMethods.get_book_by_id(id)
        if book.status_code != 200:
            return book
        try:
            query = text("""
                DELETE FROM books
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

    def update_book(model: BookDBModel, session: Session, *args, **kwargs) -> JSONResponse:
        try:
            print(model)
            query = text("""
                UPDATE books
                SET (title, authors, user_id_taken, user_reserved_id, date_start_reserve, date_start_use, date_finish_use) = 
                (:title, :authors, :user_id_taken, :user_reserved_id, :date_start_reserve, :date_start_use, :date_finish_use) 
                WHERE id = :id;
            """)
            session.execute(query, {
                "title": model.title,
                "authors": model.authors,
                "user_id_taken": model.user_id_taken,
                "user_reserved_id": model.user_reserved_id,
                "date_start_reserve": model.date_start_reserve,
                "date_start_use": model.date_start_use,
                "date_finish_use": model.date_finish_use,
                "id": model.id
            })
            return JSONResponse(
                content={
                    "details": "OK"
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={
                    "details": str(err) + ". Operation is unavailable.",
                }
            )

    def get_database(session: Session, offset: int = 0, limit: int = 15, *args, **kwargs) ->JSONResponse:
        if limit == 0:
            try: 
                query = text(
                    """
                    SELECT *
                    FROM books;
                """)
                result = session.execute(query).mappings().all()
                result_dict = CursorResultDict(result)
                return JSONResponse(
                    content={
                        'body': result_dict
                    }
                )
            except Exception as err:
                return JSONResponse(
                    status_code= 500,
                    content={
                      "details": str(err) + " . Operation is unavailable.",  
                    }
                )
        else:
            try: 
                query = text(
                    """
                    SELECT *
                    FROM books
                    LIMIT :limit
                    OFFSET :offset;
                """)
                result = session.execute(query, {
                    "limit": limit,
                    "offset": offset}).mappings().all()
                result_dict = CursorResultDict(result)
                return JSONResponse(
                    content={
                        'body': result_dict
                    }
                )
            except Exception as err:
                return JSONResponse(
                    status_code= 500,
                    content={
                      "details": str(err) + " . Operation is unavailable.",  
                    }
                )
