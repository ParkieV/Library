import json

from fastapi import APIRouter, Path
from typing import Annotated
from datetime import timedelta

from fastapi.responses import JSONResponse

from backend.user.schema import UserAuthModel, BaseAuthToken, ButtonModel
from backend.user.backends import authenticate_user, reserve_book, cancel_reserve_book, take_book, cancel_take_book
from backend.db.settings import JWTSettings
from backend.db.backends import PasswordJWT, UserMethods
from backend.db.schema import Token, AuthModel


class UserViews():
        
    user_router = APIRouter(prefix="/user")
    
    # user_router.include_router(LibrarianViews.librarian_router, tags=["librarian"])
    # user_router.include_router(AdminViews.admin_router, tags=["admin"])
    
    @user_router.post("/{user_id}/token")
    def login_for_access_token(
        user_id: Annotated[int, Path(title="id for user")],
        body: AuthModel
    ) -> JSONResponse:
        user = authenticate_user(body.email, body.password)
        if user.status_code != 200:
            return user
        else:
            print("ok")
        token = json.loads(user.body.decode("utf-8"))["user"]["access_token"]
        return Token(
            access_token=token,
            token_type="bearer")
    
    @user_router.get("/main")
    def MainView(body: UserAuthModel) -> JSONResponse:
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
    def AccountView(
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
        
    @user_router.get("/accept_take")
    def acceptTakeView(
        body: ButtonModel) -> JSONResponse:
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
            result = take_book(body.data.user_id, body.data.book_id)
            if result:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                            "query": result}
            else:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token))}
            return JSONResponse(
                content=response
            )
        

    @user_router.get("/cancel_take")
    def cancelTakeView(
        body: ButtonModel) -> JSONResponse:
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
            result = cancel_reserve_book(body.data.user_id)
            if result:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                            "query": result}
            else:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token))}
            return JSONResponse(
                content=response
            )
            
    
    @user_router.get("/accept_reserve")
    def acceptReserveView(
        body: ButtonModel) -> JSONResponse:
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
            result = reserve_book(body.data.user_id, body.data.book_id)
            if result:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                            "query": result}
            else:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token))}
            return JSONResponse(
                content=response
            )
        
    
    @user_router.get("/cancel_reserve")
    def cancelReserveView(
        body: ButtonModel) -> JSONResponse:
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
            result = cancel_reserve_book(body.data.user_id)
            if result:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token)),
                            "query": result}
            else:
                response = {"auth": UserAuthModel(auth=BaseAuthToken(email=body.auth.email,access_token=token))}
            return JSONResponse(
                content=response
            )
        