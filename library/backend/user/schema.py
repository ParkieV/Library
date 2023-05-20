from pydantic import BaseModel
from backend.db.schema import Token, TokenData

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