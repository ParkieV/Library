from pydantic import BaseModel

from backend.schemas.tokens_schemas import AuthModel


class BookQueryModel(BaseModel):
    user_id: int
    book_id: int
    type_order: str
    type_query: str

class BookQueryDBModel(BookQueryModel):
    id: int

    class Config:
        orm_mode = True


class QueryGetDeleteModel(BaseModel):
    auth: AuthModel | None = None


class QueryCreateModel(BaseModel):
    auth: AuthModel | None = None
    query: BookQueryModel | None = None
    