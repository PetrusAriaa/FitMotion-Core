from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..db import get_db
from ..model import UserModel
from ..dto import UserResponse
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel
from datetime import datetime
# from passlib.context import CryptContext

from ..utils import validate_uuid


# bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    display_name: str
    password: str

user_router = APIRouter(tags=['User'])


def __generate_passw(password: str):
    _password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(_password, salt)
    return str(hashed).split("'")[1]


@user_router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: str, db: Session=Depends(get_db)):
    _user_id, err = validate_uuid(user_id)
    if err != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err.args[0])
    user = db.query(UserModel).where(UserModel.id == _user_id).first()
    res = {
        "code": status.HTTP_200_OK,
        "data": {
            "id": str(user.id),
            "username": user.username,
            "displayName": user.display_name
        }
    }
    return JSONResponse(res, status_code=status.HTTP_200_OK)


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user ( create_user_request: CreateUserRequest,
                db : Session = Depends(get_db)):
    
    _password = __generate_passw(create_user_request.password)
    create_user_model = UserModel(
        id=uuid4(),
        display_name = create_user_request.display_name,
        username = create_user_request.username,
        password = _password,
        created_at = datetime.now()
    )

    db.add(create_user_model)
    db.commit()
    return JSONResponse({"massage" : "success"})