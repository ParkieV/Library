from app.core.security import get_password_hash

def create_first_user():
    print(get_password_hash("Qwerty123."))