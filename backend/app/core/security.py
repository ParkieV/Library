import json

from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends

from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.core.settings import EnvJWTSettings
from app.schemas.tokens import TokenData
from app.crud.users import UserMethods
from app.schemas.users import UserDBModel

settings = EnvJWTSettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
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
        if datetime.now(timezone.utc) - tokenTime > timedelta(minutes=int(settings.token_expire_minutes)):
            user.access_token = None
            user.time_token_create = None
            UserMethods.update_user(user)
            return JSONResponse(
                status_code=403,
                content={"details": "Token is outdated"}
            )
        new_token = create_access_token({"sub": auth_model.email}, timedelta(
            minutes=int(settings.token_expire_minutes)))
        return JSONResponse(
            content={"token": new_token})
    return JSONResponse(
        status_code=403,
        content={"details": "Invalid token"}
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> JSONResponse:
    credentials_exception = JSONResponse(
        status_code=401,
        content={
            "details": "Could not validate credentials"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = UserMethods.get_user_by_email(email)
    if user.status_code != 200:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[JSONResponse, Depends(get_current_user)]
):
    if current_user.status_code != 200:
        return current_user
    current_user = json.loads(current_user.body.encode["utf-8"])["user"]
    if current_user["disabled"]:
        raise JSONResponse(contents={"details": "Inactive user"})
    return current_user
