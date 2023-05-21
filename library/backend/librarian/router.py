import json

from fastapi import APIRouter
from datetime import datetime

from fastapi.responses import JSONResponse

from backend.db.backends import PasswordJWT, UserMethods
from backend.user.schema import ButtonData
from backend.db.schema import UserDBModel
from backend.librarian.backends import accept_reserve_book


class LibrarianViews():
    
    librarian_router = APIRouter("/librarian")

    @librarian_router.post("/accept_reserve")
    def accept_reserve_query(body: ButtonData) -> JSONResponse:
        
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            if client["user_type"] == "Librarian":
                client["access_token"] = token
                client["time_token_create"] = datetime.now().isoformat()
                result = UserMethods.update_user(UserDBModel.parse_obj(client))
                if result.status_code != 200:
                    return result
                response_query = accept_reserve_book(body.data.user_id, body.data.book_id)
                response_query = json.loads(response_query.body.decode('utf-8'))
                response_query["access_token"] = token
                return JSONResponse(
                    content=response_query
                )
            else:
                return JSONResponse(
                    status_code=403,
                    content={"details": "Access denied"}
                )