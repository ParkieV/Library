from pydantic import BaseModel

from backend.schemas.tokens_schemas import BaseAuthToken


class BookModel(BaseModel):
    title: str
    authors: str
    user_id_taken: int | None = None
    user_reserved_id: int | None = None
    date_start_reserve: str | None = None
    date_start_use: str | None = None
    date_finish_use: str | None = None

    class Config:
        orm_mode = True


class BookDBModel(BookModel):
    id: int


class BookGetDeleteModel(BaseModel):
    auth: BaseAuthToken | None = None


class BookCreateUpdateModel(BaseModel):
    auth: BaseAuthToken | None = None
    book: BookModel | None = None
