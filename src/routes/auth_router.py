from typing import Annotated
from os import getenv
import bcrypt
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..dto import TokenResponseModel
from ..model import Users
from ..db import get_db

auth_router = APIRouter(tags=['Authentication'])

oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def __generate_token(data: dict) -> str:
    to_encode = data.copy()
    token = jwt.encode(to_encode, getenv("SECRET"), getenv("ALGORITHM"))
    return token


def __validate_password(password: str, true_password:str) -> bool:
    b_password = password.encode(encoding='utf-8')
    return bcrypt.checkpw(b_password, bytes(true_password, encoding='utf-8'))


def validate_token(token: Annotated[str, Depends(oauth2_token_scheme)]):
    credential_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={'WWW-Authenticate': 'Bearer'}
        )
    try:
        payload = jwt.decode(token, getenv("SECRET"), getenv("ALGORITHM"))
        return payload
    except JWTError:
        raise credential_error


@auth_router.post("/login", response_model=TokenResponseModel, status_code=status.HTTP_200_OK)
def local_login(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session=Depends(get_db))  -> TokenResponseModel:
    user = None
    try:
        _ = auth_data.username.index('@') != -1
        user = db.query(Users).filter(Users.email==auth_data.username).first()
    except ValueError:
        user = db.query(Users).filter(Users.username==auth_data.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found",
                            headers={'WWW-Authenticate': 'Bearer'})

    if not __validate_password(auth_data.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Wrong username or password", headers={'WWW-Authenticate':'Bearer'})
    token = __generate_token(data={"id": str(user.id)})
    res = TokenResponseModel(
            access_token = token,
            token_type = "Bearer",
            username = user.username
            )
    return res
