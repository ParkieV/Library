from pydantic import BaseSettings

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine


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
    token_expire_minutes: str = "30"

    class Config:
        env_prefix = "JWT_"
        env_file = "app/.env"


settings = EnvDBSettings()
DATABASE_URL = f"postgresql+asyncpg://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
DB_ENGINE = create_async_engine(DATABASE_URL)
Base = declarative_base()
