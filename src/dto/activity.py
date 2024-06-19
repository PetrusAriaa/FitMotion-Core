from pydantic import BaseModel
from .response import BaseResponse

class ActivityModel(BaseModel):
    walk_min: float = 0.0
    jogging_min: float = 0.0
    stand_min: float = 0.0
    sit_min: float = 0.0
    downstair_min: float = 0.0
    upstair_min: float = 0.0

class ActivityResponseModel(BaseResponse):
    code: int
    data: ActivityModel