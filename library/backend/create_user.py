from sqlalchemy.orm import sessionmaker

from backend.models.users import Users
from backend.core.security import PasswordJWT
from backend.crud.usersCRUD import UserMethods
from backend.core.db_settings import DB_ENGINE


def create_first_user(*args, **kwargs):
    
    user = Users(
        name="Иван",
        surname="Иванов",
        email="example123@example.ru",
        hashed_password=PasswordJWT.get_password_hash("Qwerty123."),
        user_type="Admin",
    )
    Session = sessionmaker(bind=DB_ENGINE)
    session = Session()
    UserMethods.create_user(user, session)
