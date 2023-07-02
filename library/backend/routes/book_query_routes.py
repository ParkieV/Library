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
