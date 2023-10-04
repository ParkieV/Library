from datetime import UTC, datetime, timedelta

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.core.settings import token_settings
from app.crud.users import get_user_by_email
from app.schemas.tokens import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/v1/auth/login")

def create_token(data: TokenPayload, expires_delta: timedelta | None = None) -> str:
	"""Create token"""

	data.exp = datetime.now(tz=UTC) + (expires_delta or timedelta(minutes=int(token_settings.access_token_expire_minutes) or 15))

	return jwt.encode(data.dict(), token_settings.secret_key, algorithm=token_settings.algorithm)

def decode_token(token: str) -> TokenPayload | None:
	"""Decode token. On error return None"""

	try:
		encoded_jwt = TokenPayload(**jwt.decode(token, str(token_settings.secret_key), algorithms=[token_settings.algorithm]))

	except JWTError:
		return None

	return encoded_jwt

async def checkAccess(authorization: str = Header(...), session: AsyncSession = Depends(get_async_session)) -> str:
	""" Return User role.
		If user didn't auth, return Anonymous. """

	try:
		token = authorization.split("Bearer ")[1]

		if not (payload := decode_token(token)):
			return "Anonymous"


		if not (email := payload.sub):
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

		# Не понял, как сделать проверку без обращения к БД
		if not (user := await get_user_by_email(session, email)):
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

		exp_time = payload.exp
		if not exp_time:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
		elif exp_time < datetime.now(tz=UTC):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is expired")

		return user.user_type

	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid token")
