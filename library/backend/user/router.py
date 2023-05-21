import json

from fastapi import APIRouter, Path
from typing import Annotated
from datetime import datetime

from fastapi.responses import JSONResponse

from backend.user.schema import UserAuthModel, BaseAuthToken, ButtonModel
from backend.user.backends import authenticate_user, reserve_book, cancel_reserve_book, take_book, cancel_take_book
from backend.db.backends import PasswordJWT, UserMethods
from backend.db.schema import Token, AuthModel, UserDBModel


class UserViews():
        
    user_router = APIRouter(prefix="/user")
    
    # user_router.include_router(LibrarianViews.librarian_router, tags=["librarian"])
    
    @user_router.post("/{user_id}/token")
    def login_for_access_token(
        user_id: Annotated[int, Path(title="id for user")],
        body: AuthModel
    ) -> JSONResponse:
        user = authenticate_user(body.email, body.password, user_id)
        if user.status_code != 200:
            return user
        token = json.loads(user.body.decode("utf-8"))["user"]["access_token"]
        return Token(
            access_token=token,
            token_type="bearer")
    
    @user_router.get("/main")
    def main_view(body: UserAuthModel) -> JSONResponse:
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
            token = json.loads(auth_result.body.decode["utf-8"])["token"]
            user = UserMethods.get_user_by_email(body.auth.email)
            if user.status_code != 200:
                return user
            user = json.loads(user.body.decode["utf-8"])["user"]
            user = {
                "id": user["id"],
                "name": user["name"],
                "surname": user["surname"],
                "book_id_taken": user["book_id_taken"],
                "reserved_book_id": user["reserved_book_id"]
            }
            response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                        "user": user}
            return JSONResponse(
                content=response
            )
    
    @user_router.get("/{user_id}")
    def account_view(
        user_id: Annotated[int, Path(title="ID for user")],
        body: UserAuthModel) -> JSONResponse:
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
            token = json.loads(auth_result.body.decode["utf-8"])["token"]
            user = UserMethods.get_user_by_email(body.auth.email)
            
            if user.status_code != 200:
                return user
            user = json.loads(user.body.decode["utf-8"])["user"]
            user = UserDBModel.parse_obj(user)
            response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                        "user": user}
            return JSONResponse(
                content=response
            )
        
    @user_router.post("/send_take")
    def send_take_view(body: ButtonModel) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            client["access_token"] = token
            client["time_token_create"] = datetime.now().isoformat()
            result = UserMethods.update_user(UserDBModel.parse_obj(client))
            if result.status_code != 200:
                return result
            if client["id"] != body.data.user_id:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"}
                )
            response_query = take_book(body.data.user_id, body.data.book_id)
            response_query = json.loads(response_query.body.decode('utf-8'))
            response_query["access_token"] = token
            return JSONResponse(
                content=response_query
            )
        

    @user_router.post("/send_cancel_take")
    def cancel_take_view(body: ButtonModel) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            client["access_token"] = token
            client["time_token_create"] = datetime.now().isoformat()
            result = UserMethods.update_user(UserDBModel.parse_obj(client))
            if result.status_code != 200:
                return result
            if client["id"] != body.data.user_id:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"}
                )
            response_query = cancel_take_book(body.data.user_id, body.data.book_id)
            response_query = json.loads(response_query.body.decode('utf-8'))
            response_query["access_token"] = token
            return JSONResponse(
                content=response_query
            )
            
    
    @user_router.post("/send_reserve")
    def accept_reserve_view(body: ButtonModel) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            client["access_token"] = token
            client["time_token_create"] = datetime.now().isoformat()
            result = UserMethods.update_user(UserDBModel.parse_obj(client))
            if result.status_code != 200:
                return result
            if client["id"] != body.data.user_id:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"}
                )
            response_query = reserve_book(body.data.user_id, body.data.book_id)
            response_query = json.loads(response_query.body.decode('utf-8'))
            response_query["access_token"] = token
            return JSONResponse(
                content=response_query
            )
        
    
    @user_router.post("/cancel_reserve")
    def cancel_reserve_view(body: ButtonModel) -> JSONResponse:
        auth_result = PasswordJWT.check_access_token(body.auth)
        if auth_result.status_code != 200:
            return auth_result
        else:
            client = UserMethods.get_user_by_email(body.auth.email)
            if client.status_code != 200:
                return client
            token = json.loads(auth_result.body.decode('utf-8'))["token"]
            client = json.loads(client.body.decode('utf-8'))["user"]
            client["access_token"] = token
            client["time_token_create"] = datetime.now().isoformat()
            result = UserMethods.update_user(UserDBModel.parse_obj(client))
            if result.status_code != 200:
                return result
            if client["id"] != body.data.user_id:
                return JSONResponse(
                    status_code=403,
                    content={
                        "details": "Access denied"}
                )
            response_query = cancel_reserve_book(client["email"], body.data.user_id, body.data.book_id)
            response_query = json.loads(response_query.body.decode('utf-8'))
            response_query["access_token"] = token
            return JSONResponse(
                content=response_query
            )
        