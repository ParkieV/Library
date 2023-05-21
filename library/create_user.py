from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from backend.db.models import Users
from backend.db.schema import UserDBModel
from backend.db.backends import PasswordJWT, UserMethods
from backend.db.settings import DBSettings


def main(*args, **kwargs):
    user = Users(
        name="Степан",
        surname="Пискунов",
        email="example123@example.ru",
        hashed_password=PasswordJWT.get_password_hash("Qwerty123."),
        user_type="Admin",
    )
    UserMethods.create_user(user)


if __name__=="__main__":
    main()