from passlib.context import CryptContext
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


class EnvDBSettings(BaseSettings):
	username: str
	password: str
	database: str
	host: str
	port: str

	class Config:
		env_prefix = "DB_"
		env_file = "app/.env"


class EnvJWTSettings(BaseSettings):
	secret_key: str
	algorithm: str
	access_token_expire_minutes: str = "30"
	refresh_token_expire_days: str = "60"

	class Config:
		env_prefix = "JWT_"
		env_file = "app/.env"


token_settings = EnvJWTSettings() # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = EnvDBSettings() # type: ignore

DATABASE_URL = f"postgresql+asyncpg://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
DB_ENGINE = create_async_engine(DATABASE_URL)
Base = declarative_base()
