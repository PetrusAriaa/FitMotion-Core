import uuid
from .response import BaseResponse
from pydantic import BaseModel

class UserData(BaseModel):
    id: uuid.UUID
    username: str
    displayName: str

class UserResponse(BaseResponse):
    data: UserData