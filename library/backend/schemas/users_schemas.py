from pydantic import BaseModel, EmailStr

from backend.schemas.tokens_schemas import BaseAuthToken, Token, TokenData


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

class BaseAuthToken(Token, TokenData):
    pass


class UserAuthModel(BaseModel):
    auth: BaseAuthToken | None = None

    class Config:
        orm_mode = True

class ButtonData(BaseModel):
    user_id: int
    book_id: int


class ButtonModel(BaseModel):
    auth: BaseAuthToken
    data: ButtonData