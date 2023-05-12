import re

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from backend.db.schema import User, Book
from backend.db.models import Users, Books
from backend.db.settings import DBSettings


class UserMethods():
    def setUp(func) -> None:
        def _wrapper(*args, **kwargs):
            settings = DBSettings()
            engine = create_engine(f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}")
            session = sessionmaker(bind=engine)
            kwargs['session'] = session
            result = func(*args, **kwargs)
            session.commit()
            session.close()
            return result
        return _wrapper
    
    @staticmethod
    def _email_validation(email:str) -> bool:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(email_regex, email)
    
    @staticmethod
    def _auth_validation(email: str, password: str) -> bool:
        if not UserMethods._email_validation(email):
            return False
        password_regex = re.compile('^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
        if not re.fullmatch(password_regex, password):
            return False
        return True
    
    @setUp
    def get_user_by_email(email: str, *args, **kwargs) -> User | None:
        session = kwargs["session"]
        if not UserMethods._email_validation(email):
            return {
                'status': 500,
                'message': 'Invalid email.'
            }
        result = session.query(Users).filter(Users.email == email).first()
        if result:
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        return {
            'status': 500,
            'message': 'User not found.',
            'body': None
        }
    
    @setUp
    def create_user(model: User, *args, **kwargs) -> dict:
        session = kwargs["session"]
        if not UserMethods._auth_validation(model.email, model.password):
            return {
                'status': 500,
                'message': 'Invalid email or password.'
            }
        if UserMethods.get_user_by_email(model.email)['status'] != 500:
            return {
                'status': 500,
                'message': 'User already exists.'
            }
        try:
            session.add(model)
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable."
            }
        return {
            'status': 200,
            'message': 'OK'
        }

    @setUp
    def get_user_by_id(id: int, *args, **kwargs) -> User | None:
        session = kwargs["session"]
        result = session.query(Users).filter(Users.id == id).first()
        if result:
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        return {
            'status': 500,
            'message': 'User not found.',
            'body': None
        }

    @setUp
    def update_user(model: User, *args, **kwargs) -> dict:
        session = kwargs["session"]
        user = UserMethods.get_user_by_id(model.id)
        if user['status'] != 200:
            return user
        try:
            stmt = (
                update(Users).
                where(Users.id == model.id).
                values(model.dict(exclude_unset=True)).
                returning(Users)
            )
            result = session.execute(stmt)
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable.",
                'body': None
            }

    def delete_user_by_id(id:int, *args, **kwargs) -> dict:
        session = kwargs["session"]
        user = UserMethods.get_user_by_id(id)
        if user['status'] != 200:
            return user
        try:
            request = Users.query.filter(Users.id == id).first()
            session.delete(request)
            return {
                'status': 200,
                'message': 'OK',
            }
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable."
            }


class BookMethods():
    def setUp(func) -> None:
        def _wrapper(*args, **kwargs):
            engine = create_engine("postgresql+psycopg2://postgres:5432@localhost/library_db")
            session = sessionmaker(bind=engine)
            kwargs['session'] = session
            result = func(*args, **kwargs)
            session.commit()
            session.close()
            return result
        return _wrapper
    
    @setUp
    def search_book_by_title(title: str, *args, **kwargs) -> dict:
        session = kwargs["session"]
        result = Books.query.filter(Books.title.match(title)).limit(10)
        try:
            result = session.execute(result)
            if not result:
                return {
                    'status': 500,
                    'message': 'Book not found.',
                    'body': None
                }
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable.",
                'body': None
            }

    @setUp
    def create_book(model: Book, *args, **kwargs) -> dict:
        session = kwargs["session"]
        if not model.user_id_taken:
            if UserMethods.get_user_by_id(model.user_id_taken)['status'] != 200:
                return {
                    'status': 500,
                    'message': 'Uncorrect values.'
                }
        if not model.user_reserved_id:
            if UserMethods.get_user_by_id(model.user_reserved_id)['status'] != 200:
                return {
                    'status': 500,
                    'message': 'Uncorrect values.'
                }
        try:
            session.add(model)
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable."
            }
        return {
            'status': 200,
            'message': 'OK'
        }

    @setUp
    def get_book_by_id(id: int, *args, **kwargs) -> dict:
        session = kwargs['session']
        result = session.query(Books).filter(Books.id == id).first()
        if result:
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        else:
            return {
                'status': 500,
                'message': 'User not found.',
                'body': None
            }

    @setUp
    def delete_book_by_id(id: int, *args, **kwargs):
        session = kwargs['session']
        book = BookMethods.get_book_by_id(id)
        if book['status'] != 200:
            return book
        try:
            request = Books.query.filter(Books.id == id).first()
            session.delete(request)
            return {
                'status': 200,
                'message': 'OK',
            }
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable."
            }

    @setUp
    def update_book(model: Book, *args, **kwargs) -> dict:
        session = kwargs["session"]
        book = BookMethods.get_book_by_id(model.id)
        if book['status'] != 200:
            return book
        try:
            stmt = (
                update(Books).
                where(Books.id == model.id).
                values(model.dict(exclude_unset=True)).
                returning(Books)
            )
            result = session.execute(stmt)
            return {
                'status': 200,
                'message': 'OK',
                'body': result
            }
        except Exception as err:
            return {
                'status': 500,
                'message': err + " . Operation is unavailable.",
                'body': None
            }
