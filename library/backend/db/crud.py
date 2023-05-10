import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from backend.db.schema import User as schema
from backend.db.models import Users as model


class UserCRUD():
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
    
    def _email_validation(email:str) -> bool:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(email_regex, model.email)

    @setUp
    def create_user(meta_model: schema, model: schema, *args, **kwargs):
        session = kwargs['session']
        if meta_model.user_type != 'Admin':
            return {
                'status': 403,
                'message': 'Access denied.'
            }
        if not UserCRUD._email_validation(model.email):
            return {
                'status': 500,
                'message': 'Invalid email.'
            }
        password_regex = re.compile('^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
        if not re.fullmatch(password_regex, model.password):
            return {
                'status': 500,
                'message': 'Invalid password.'
            }
        if model.user_type == 'Admin':
            return {
                'status': 403,
                'message': 'Access denied.'
            }
        session.add(model)
        return {
            'status': 200,
            'message': 'OK'
        }

    @setUp
    def get_user_by_email(meta_model: schema, email: str, *args, **kwargs):
        session = kwargs['session']
        if meta_model.user_type != 'Admin' and meta_model.user_type != 'User' and meta_model.user_type != 'Librarian':
            return {
                'status': 403,
                'message': 'Access denied.'
            }
        if not UserCRUD._email_validation(email):
            return {
                'status': 500,
                'message': 'Invalid email.'
            }
        result = session.query(model.BaseUser).filter(model.BaseUser.email == email).first()
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


    def update_user_by_email(meta_model: schema, email: str, model: schema, *args, **kwargs):
        if meta_model.user_type != 'Admin' and meta_model.user_type != 'User' and meta_model.user_type != 'Librarian':
            return {
                'status': 403,
                'message': 'Access denied.'
            }
        user = UserCRUD.get_user_by_email(meta_model, email)
        if user['status'] != 200:
            return user
        return UserCRUD.create_user(meta_model, model)

    @setUp
    def delete_user_by_email(meta_model: schema, email:schema, *args, **kwargs):
        session = kwargs['session']
        if meta_model.user_type != 'Admin' and meta_model.user_type != 'User' and meta_model.user_type != 'Librarian':
            return {
                'status': 403,
                'message': 'Access denied.'
            }
        if not UserCRUD._email_validation(email):
            return {
                'status': 500,
                'message': 'Invalid email.'
            }
        result = session.query(model.BaseUser).filter(model.BaseUser.email == email).first()
        if not result:
            return {
                'status': 500,
                'message': 'User not found.',
            }
        session.delete(result)
        return {
            'status': 200,
            'message': 'OK'
        }