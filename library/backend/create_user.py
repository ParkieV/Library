from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users_schemas import UserHashedModel
from backend.crud.usersCRUD import UserMethods
from backend.core.db_settings import DB_ENGINE
from backend.methods.token_methods import PasswordJWT


async def create_first_user(session: AsyncSession = AsyncSession(DB_ENGINE, expire_on_commit=False)):
    
    user = UserHashedModel(
        name="Иван",
        surname="Иванов",
        email="example123@example.ru",
        user_type="Admin",
        hashed_password=PasswordJWT.get_password_hash("Qwerty123."),
    )
    return await UserMethods.create_user(session, user)
