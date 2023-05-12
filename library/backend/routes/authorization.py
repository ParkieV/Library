from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from backend.db import schema
from backend.db.crud import UserCRUD as crud


router = APIRouter()

@router.post("/auth/", response_model=schema.User)
def authentification(user: schema.UserAuth):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user(user)