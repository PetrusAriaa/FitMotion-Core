from typing import Annotated, Any
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .auth_router import validate_token
from ..db import get_db
from ..model import Users, Friends
from ..dto import CommonUserModel, CreateUserRequest, CommonUserResponseModel,\
    FriendRequestsModel, FriendRequestsResponseModel, UserInfoRequest, \
    FriendsResponseModel, FriendsModel
from sqlalchemy.orm import Session
import bcrypt
from datetime import datetime


user_router = APIRouter(tags=['User'])


def __generate_passw(password: str):
    _password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(_password, salt)
    return str(hashed).split("'")[1]


@user_router.get('/search', response_model=CommonUserResponseModel)
def get_user(username: str, db: Session=Depends(get_db)):
    user_list = []
    if not len(username) > 0:
        res = CommonUserResponseModel(
            code=status.HTTP_200_OK,
            data=user_list
        )
        return res
    try:
        users = db.query(Users).filter(Users.username.contains(username)).limit(10).all()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="IDK BRO YO SERVER SUCKS")
    for user in users:
        _user = user.__dict__
        user_list.append(CommonUserModel(**_user))
    
    res = CommonUserResponseModel(
        code=status.HTTP_200_OK,
        data=user_list
    )
    return res


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user ( create_user_request: CreateUserRequest,
                db : Session = Depends(get_db)):
    
    _password = __generate_passw(create_user_request.password)
    
    user = db.query(Users).where(Users.username == create_user_request.username).first()
    if user is not None:
        raise HTTPException(400, detail="Username tidak dapat digunakan. Gunakan username lain.")
    
    user = db.query(Users).where(Users.email == create_user_request.email).first()
    if user is not None:
        raise HTTPException(400, detail="Email ini sudah terdaftar. Gunakan email lain.")
    try:
        create_user_model = Users(
            id=uuid4(),
            username = create_user_request.username,
            email = create_user_request.email,
            password = _password,
            created_at = datetime.now()
        )
        db.add(create_user_model)
        db.commit()
        return JSONResponse({"message" : "success"})
    except Exception as e:
        print(e)
        raise HTTPException(500, detail="Internal Server Error")


def __validate_sex(sex_type: str):
    try:
        _ = ['F', 'M', 'm', 'F'].index(sex_type)
    except ValueError:
        raise HTTPException(400, detail="Sex must be one of 'F', 'M', 'm', 'f'.")


def __validate_goal(goal_type: str):
    try:
        _ = ['A', 'B'].index(goal_type)
    except ValueError:
        raise HTTPException(400, detail="Goal must be either A or B.")


@user_router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def edit_info(base_info: UserInfoRequest,
                session: Annotated[dict[str, Any], Depends(validate_token)],
                db: Session = Depends(get_db)):
    user_id = session['id']
    __validate_sex(base_info.sex)
    __validate_goal(base_info.goal)
    try:
        user = db.query(Users).where(Users.id == user_id).first()
        if user is None:
            raise HTTPException(404, detail="Username tidak ditemukan.")
        user.height = base_info.height
        user.weight = base_info.weight
        user.birth = base_info.birth
        user.sex = base_info.sex
        user.fk_goal = base_info.goal
        user.updated_at = datetime.now()
        db.commit()
        return JSONResponse({"message" : "success"})
    except Exception as e:
        print(e)
        raise HTTPException(500, detail="Internal Server Error")


@user_router.get("/requests", response_model=FriendRequestsResponseModel)
def get_friends_requests(session: Annotated[dict[str, ], Depends(validate_token)],
                        db: Session = Depends(get_db)):
    requests_list = []
    requests = db.execute(
        text(f"""
            SELECT fr.id AS id,  u.username AS username, fr.created_at AS created_at FROM friend_requests fr
                JOIN users u ON u.id = fr.friend_id
                WHERE fk_user_id='{str(session['id'])}';
        """)
    )
    for request in requests:
        _request = request._asdict()
        requests_list.append(FriendRequestsModel(**_request))
    
    res = FriendRequestsResponseModel(
        code=status.HTTP_200_OK,
        data=requests_list
    )
    return res


@user_router.get("/friends", response_model=FriendsResponseModel)
def get_friends_list(session: Annotated[dict[str, Any], Depends(validate_token)],
                    db: Session = Depends(get_db)):
    user_id = session['id']
    friends_list = []
    friends = db.execute(
        text(f"""
            SELECT fr.id AS id,  u.username AS username, fr.created_at AS created_at FROM friends fr
                JOIN users u ON u.id = fr.friend_id
                WHERE fk_user_id='{str(user_id)}';
        """)
    )
    for request in friends:
        _request = request._asdict()
        friends_list.append(FriendsModel(**_request))
    
    res = FriendsResponseModel(
        code=status.HTTP_200_OK,
        data=friends_list
    )
    return res