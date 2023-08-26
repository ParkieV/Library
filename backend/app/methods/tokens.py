from datetime import UTC, datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import token_settings
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
