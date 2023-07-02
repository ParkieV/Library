import json

from sqlalchemy import create_engine, text, CursorResult
from pydantic import EmailStr
from typing import List, Annotated
from datetime import datetime, timedelta, date, timezone
from dateutil import parser
from jose import JWTError, jwt
from fastapi import Depends

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.db.schema import UserDBModel, BookDBModel, AuthModel
from backend.db.schema import TokenData
from backend.db.models import Users, Books, BookQuery
from backend.db.settings import DBSettings, JWTSettings


class PasswordJWT():

    settings = JWTSettings()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(plain_password, hashed_password):
        return PasswordJWT.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return PasswordJWT.pwd_context.hash(password)
    
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, PasswordJWT.settings.secret_key, algorithm=PasswordJWT.settings.algorithm)
        return encoded_jwt

    def check_access_token(auth_model: TokenData, *args, **kwargs):
        user = UserMethods.get_user_by_email(auth_model.email)
        if user.status_code != 200:
            return JSONResponse(
                status_code=403,
                content={"details": "User not found"}
            )
        user = UserDBModel.parse_obj(json.loads(user.body.decode("utf-8"))["user"])
        if auth_model.access_token == user.access_token:
            user.time_token_create = user.time_token_create[1:-1]
            tokenTime = datetime.fromisoformat(user.time_token_create)
            if datetime.now(timezone.utc) - tokenTime > timedelta(minutes=int(PasswordJWT.settings.token_expire_minutes)):
                user.access_token = None
                user.time_token_create = None
                UserMethods.update_user(user)
                return JSONResponse(
                    status_code=403,
                    content={"details": "Token is outdated"}
                )
            new_token = PasswordJWT.create_access_token({"sub": auth_model.email}, timedelta(minutes=int(PasswordJWT.settings.token_expire_minutes)))
            return JSONResponse(
                content={"token": new_token})
        return JSONResponse(
            status_code=403,
            content={"details": "Invalid token"}
        )
