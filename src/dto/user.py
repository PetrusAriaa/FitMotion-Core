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
    commitment: Union[str, None] = None

class FriendRequestsModel(BaseModel):
    id: int
    username: str
    created_at: date

class FriendRequestsResponseModel(BaseResponse):
    data: Iterable[FriendRequestsModel]

class FriendsModel(BaseModel):
    id: int
    username: str

class FriendsResponseModel(BaseResponse):
    data: Iterable[FriendsModel]

class UserInfoModel(BaseModel):
    username : str
    weight: float
    height: float
    bmi: float
    goal: Union[str, None]
    commitment: Union[str, None]
    bmi_category: str
    recommendation: str

class UserInfoResponseModel(BaseResponse):
    code: int
    data: UserInfoModel