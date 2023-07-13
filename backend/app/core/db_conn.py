from fastapi import HTTPException, status
from sqlalchemy import text

from sqlalchemy.exc import StatementError, IntegrityError


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import DB_ENGINE, Base

from app.methods.error_handler import sql_validation_error


async def initialization_database():
    async with DB_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_connection():
    async with AsyncSession(DB_ENGINE, expire_on_commit=False) as session:
        query = text("""SELECT 1;""")

        await session.execute(query)
        await session.commit()

async def get_async_session():
    async with AsyncSession(DB_ENGINE, expire_on_commit=False) as session:
        try:
            yield session
        except IntegrityError as database_error:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=sql_validation_error(database_error))