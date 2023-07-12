from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import UserHashedModel
from app.crud.users import UserMethods
from app.core.settings import DB_ENGINE
from app.methods.token import get_password_hash


async def create_first_user(session: AsyncSession = AsyncSession(DB_ENGINE, expire_on_commit=False)):
    
    user = UserHashedModel(
        name="Иван",
        surname="Иванов",
        email="example123@example.ru",
        user_type="Admin",
        hashed_password=get_password_hash("Qwerty123."),
    )
    return await UserMethods.create_user(session, user)