from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from backend.db.models import Users
from backend.db.schema import UserDBModel
from backend.db.backends import PasswordJWT
from backend.db.settings import DBSettings



def setUp(func) -> None:
    def _wrapper(*args, **kwargs):
        settings = DBSettings()
        engine = create_engine(f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}")
        session = Session(bind=engine)
        kwargs['session'] = session
        result = func(*args, **kwargs)
        session.commit()
        session.close()
        return result
    return _wrapper


@setUp
def main(*args, **kwargs):
    user = Users(
        name="Степан",
        surname="Пискунов",
        email="st-psk@mail.ru",
        hashed_password=PasswordJWT.get_password_hash("Qwerty123."),
        user_type="Admin",
    )
    session = kwargs["session"]
    session.add(user)


if __name__=="__main__":
    main()