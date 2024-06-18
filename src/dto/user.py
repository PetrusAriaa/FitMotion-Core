from typing import Iterable, Union
from datetime import date
import uuid
from .response import BaseResponse
from pydantic import BaseModel

class CommonUserModel(BaseModel):
    id: uuid.UUID
    username: str

class CommonUserResponseModel(BaseResponse):
    data: Iterable[CommonUserModel]

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class UserInfoRequest(BaseModel):
    height: float
    weight: float
    birth: date
    sex: str
    goal: Union[str, None] = None

class FriendRequestsModel(BaseModel):
    id: int
    username: str
    created_at: date

class FriendRequestsResponseModel(BaseResponse):
    data: Iterable[FriendRequestsModel]

class FriendListModel(BaseModel):
    id: int
    username: str