from pydantic import BaseModel


class ErrorModel(BaseModel):
    error_type: str
    error_details: str