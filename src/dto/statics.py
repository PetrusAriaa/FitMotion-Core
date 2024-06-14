from typing import Iterable
from pydantic import BaseModel
from .response import BaseResponse

class StaticGoalModel(BaseModel):
    id: str
    name: str
    description: str

class StaticGoalResponseModel(BaseResponse):
    code: int
    data: Iterable[StaticGoalModel]

class StaticIllnessModel(BaseModel):
    id: str
    name: str

class StaticIllnessResponseModel(BaseResponse):
    code: int
    data: Iterable[StaticIllnessModel]