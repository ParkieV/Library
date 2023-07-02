import json

from sqlalchemy import create_engine, text, CursorResult
from pydantic import EmailStr
from typing import List, Annotated
from datetime import datetime, timedelta, date, timezone
from dateutil import parser
from jose import JWTError, jwt
from fastapi import Depends

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.db.schema import UserDBModel, BookDBModel, AuthModel
from backend.db.schema import TokenData
from backend.db.models import Users, Books, BookQuery
from backend.db.settings import DBSettings, JWTSettings


def CursorResultDict(obj: CursorResult | List[CursorResult], *args, **kwargs) -> dict:
    if type(obj) is list:
        result_keys, result_items = [elem.keys() for elem in obj], [elem.items() for elem in obj]
        result_dict = []
        for i in range(len(result_keys)):
            result_dict.append(dict(zip(result_keys[i], result_items[i])))
        for i in range(len(result_dict)):
            for key in result_dict[i].keys():
                result_dict[i][key] = result_dict[i][key][1:]
                if len(result_dict[i][key]) == 1:
                    result_dict[i][key] = result_dict[i][key][0]
    else:
        result_keys, result_items = obj.keys(), obj.items()
        result_dict = dict(zip(result_keys, result_items))
        for key in result_dict.keys():
            result_dict[key] = result_dict[key][1:]
            if len(result_dict[key]) == 1:
                result_dict[key] = result_dict[key][0]
    return result_dict


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
