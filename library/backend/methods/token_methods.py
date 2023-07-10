from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from backend.core.token_settings import EnvJWTSettings


class PasswordJWT():

    settings = EnvJWTSettings()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(plain_password, hashed_password):
        return PasswordJWT.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return PasswordJWT.pwd_context.hash(password)
