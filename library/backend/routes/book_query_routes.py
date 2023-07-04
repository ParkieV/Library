import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.schemas.book_query_schemas import QueryGetDeleteModel, QueryCreateModel
from backend.models.bookQuery import BookQuery
from backend.core.token_settings import EnvJWTSettings
from backend.crud.bookQueryCRUD import BookQueryMethods


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
        auth_result = EnvJWTSettings.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
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
        auth_result = EnvJWTSettings.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        query = BookQuery(**body.query.dict())
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
        auth_result = EnvJWTSettings.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Access denied",
                    "user": {"user_type": "AnonymousUser"}
                }
            )
        else:
            return BookQueryMethods.delete_bookQuery_by_id(query_id)
