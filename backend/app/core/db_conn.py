from sqlalchemy.exc import StatementError, IntegrityError
from pydantic.errors import In

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import DB_ENGINE

async def check_connection():
    async_conn = await DB_ENGINE.connect()
    if not async_conn:
        raise StatementError("Database connection can't be established")

async def get_async_session():
    async with AsyncSession(DB_ENGINE, expire_on_commit=False) as session:
        try:
            yield session
        except StatementError as databaseError:
            await session.rollback()