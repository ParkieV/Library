from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_conn import get_async_session
from app.core.security import verify_password
from app.core.settings import token_settings
from app.crud.users import get_user_by_email
from app.methods.tokens import create_token, decode_token
from app.schemas.tokens import RefreshTokenModel, TokenPayload, TokensModel
from app.schemas.users import loginData

routes = APIRouter(prefix="/auth")


@routes.post("/login", response_model=TokensModel)
async def login(data: loginData, session: AsyncSession = Depends(get_async_session)) -> TokensModel:

	user_response = await get_user_by_email(session, data.email)
	if not user_response:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Uncorrect email")

	if not verify_password(data.password, user_response.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Uncorrect")

	payload = TokenPayload(
		sub=data.email,
		exp= datetime.now(tz=UTC) + timedelta(days=60))

	tokens = TokensModel(
		access_token=create_token(payload, timedelta(minutes=int(token_settings.access_token_expire_minutes))),
		refresh_token=create_token(payload, timedelta(days=int(token_settings.refresh_token_expire_days))))

	return tokens

@routes.post("/refresh", response_model=TokensModel)
async def refresh_tokens(refresh_token: RefreshTokenModel, session = Depends(get_async_session)) -> TokensModel:

	if not (payload := decode_token(refresh_token.refresh_token)):
		raise JWTError
	print(payload)
	if not (payload.sub):
		raise JWTError

	if not payload.exp:
		raise JWTError

	user_response = await get_user_by_email(session, payload.sub)
	if not user_response:
		raise JWTError

	new_payload = TokenPayload(
		sub=user_response.email,
		exp= datetime.now(tz=UTC) + timedelta(days=60))

	tokens = TokensModel(
		access_token=create_token(new_payload, timedelta(minutes=int(token_settings.access_token_expire_minutes))),
		refresh_token=create_token(new_payload, timedelta(days=int(token_settings.refresh_token_expire_days))))

	return tokens
