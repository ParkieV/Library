from pydantic import BaseModel, EmailStr

from backend.schemas.auth_schemas import BaseAuthToken


class BaseUserModel(BaseModel):
    name: str
    surname: str
    last_name: str | None = None
    email: EmailStr
    user_type: str = "User"
    book_id_taken: int | None = None
    reserved_book_id: int | None = None
    access_token: str | None = None
    time_token_create: str | None = None



class UserModel(BaseUserModel):
    password: str


class UserHashedModel(BaseUserModel):
    hashed_password: str


class UserDBModel(UserHashedModel):
    id: int

    class Config:
        orm_mode = True



class UserGetDeleteModel(BaseModel):
    auth: BaseAuthToken | None = None


class UserCreateUpdateModel(BaseModel):
    auth: BaseAuthToken | None = None
    user: UserModel | None = None