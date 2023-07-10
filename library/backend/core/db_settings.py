from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class EnvDBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = "backend/.env"


settings = EnvDBSettings()
DATABASE_URL = f"postgresql+asyncpg://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
DB_ENGINE = create_async_engine(DATABASE_URL)
Base = declarative_base()

async def initialization_database():
    async with DB_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session():
    async with AsyncSession(DB_ENGINE, expire_on_commit=False) as session:
        yield session