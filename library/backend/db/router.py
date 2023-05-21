import json
from fastapi import APIRouter, Path
from typing import Annotated
from datetime import datetime
from fastapi.responses import JSONResponse

from backend.db.schema import BookGetDeleteModel, BookCreateUpdateModel, UserDBModel, UserHashedModel
from backend.db.backends import BookMethods, UserMethods, BookQueryMethods, PasswordJWT
from backend.db.schema import BookQueryModel, QueryGetDeleteModel, QueryCreateModel
from backend.db.models import Books as BookDB
from backend.db.models import Users as UserDB
from backend.db.schema import UserGetDeleteModel, UserCreateUpdateModel
from backend.user.schema import UserAuthModel


class BooksDBViews():

    books_router = APIRouter(prefix="/books")

    @books_router.get("/action")
    def get_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            client = json.loads(auth_result.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                return BookMethods.get_book_by_id(book_id)
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )

    @books_router.post("/action")
    def update_book(
        book_id : int = 0,
        body: BookCreateUpdateModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            user = json.loads(body.body.decode('utf-8'))["user"]
            if user["user_type"] == 'Librarian':
                if BookMethods.get_book_by_id(book_id).status_code == 200:
                    book_db = BookDB(**body.book.dict())
                    book_db.id = book_id
                    return BookMethods.update_book(book_db)
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "details": "Uncorrect request"
                        }
                    )
            else:
                return JSONResponse(
                    status_code=403,
                    content = {
                        "details": "Access denied"
                    }
                )

    @books_router.put("/action")
    def create_book(body: BookCreateUpdateModel) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
        client = json.loads(auth_result.body.decode('utf-8'))["user"]
        if client["user_type"] == "Librarian":
            book = BookDB(**body.book.dict())
            return BookMethods.create_book(book)
        else:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied"
                }
            )

    @books_router.delete("/action")
    def delete_book(
        book_id: int = 0,
        body: BookGetDeleteModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            client = json.loads(auth_result.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                return BookMethods.delete_book_by_id(book_id)
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )


class UsersDBViews():

    users_router = APIRouter(prefix="/users")

    @users_router.get("/action")
    def get_user(
        user_id: int = 0,
        body: UserAuthModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["id"] != user_id:
                return JSONResponse(
                    status_code=400,
                    content={"details": "Uncorrect request"}
                )
            if client["user_type"] == "Admin" or client["id"] == user_id:
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_user = UserMethods.get_user_by_id(user_id)
                response_user = json.loads(response_user.body.decode('utf-8'))
                response_user["access_token"] = token
                return JSONResponse(
                    content=response_user
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )
 
    @users_router.delete("/action")
    def delete_user(
        user_id: int = 0,
        body: UserAuthModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Admin" or client["id"] == user_id:
                client["access_token"] = token
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_user = UserMethods.delete_user_by_id(user_id)
                response_user = json.loads(response_user.body.decode('utf-8'))
                response_user["access_token"] = token
                return JSONResponse(
                    content=response_user
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )

    @users_router.put("/action")
    def create_user(body: UserCreateUpdateModel) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Admin":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                user = body.user.dict()
                user["hashed_password"] = PasswordJWT.get_password_hash(user["password"])
                user.pop("password")
                user = UserHashedModel.parse_obj(user)
                user = UserDB(**user.dict())
                response_user = UserMethods.create_user(user)
                response_user = json.loads(response_user.body.decode('utf-8'))
                response_user["access_token"] = token
                return JSONResponse(
                    content=response_user
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"
                    }
                )

    @users_router.post("/action")
    def update_user(
        user_id : int = 0,
        body: UserCreateUpdateModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Admin" or client["id"] == user_id:
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                if UserMethods.get_user_by_id(user_id).status_code == 200:
                    user = body.user.dict()
                    user["hashed_password"] = PasswordJWT.get_password_hash(user["password"])
                    user.pop("password")
                    user["id"] = user_id
                    user = UserDBModel.parse_obj(user)
                    response_user = UserMethods.update_user(user)
                    response_user = json.loads(response_user.body.decode('utf-8'))
                    response_user["access_token"] = token
                    return JSONResponse(
                        content=response_user
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "message": "Uncorrect request"
                        }
                    )
            else:
                return JSONResponse(
                    status_code=403,
                    content = {
                        'message': 'Access denied'
                    }
                )


class BookQueriesDBViews():

    queries_router = APIRouter(prefix="/queries")

    @queries_router.get("/action")
    def get_query(query_id: int = 0,
                  body: QueryGetDeleteModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            return BookQueryMethods.get_bookQuery_by_id(query_id)

    @queries_router.put("/action")
    def create_query(body: QueryCreateModel) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
        query = BookDB(**body.query.dict())
        return BookQueryMethods.create_bookQuery(query)

    @queries_router.delete("/action")
    def delete_query(
        query_id: int = 0,
        body: QueryGetDeleteModel = None) -> JSONResponse:
        if not body:
            return JSONResponse(
                status_code=400,
                content={
                    "details": "Uncorrect request."
                }
            )
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            token = json.loads(auth_result.body.decode("utf-8"))["token"]
            return BookQueryMethods.delete_bookQuery_by_id(query_id)
