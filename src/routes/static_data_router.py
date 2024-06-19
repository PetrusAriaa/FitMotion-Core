from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from ..db import get_db
from ..dto import StaticGoalModel, StaticGoalResponseModel, StaticIllnessModel, StaticIllnessResponseModel, StaticCommitmentModel, StaticCommitmentResponseModel
from ..model import Illness, Goals, Commitment

static_data_router = APIRouter(tags=['Utilities'])

@static_data_router.get('/illness', response_model=StaticIllnessResponseModel, deprecated=True)
def get_illness_type(db: Session=Depends(get_db)):
    illness_list = []
    illness = db.query(Illness).all()
    for item in illness:
        illness_list.append(StaticIllnessModel(**item.__dict__))
    res = StaticIllnessResponseModel(
        code=status.HTTP_200_OK,
        data=illness_list
    )
    return res


@static_data_router.get('/goal', response_model=StaticGoalResponseModel)
def get_goal_type(db: Session=Depends(get_db)):
    goals_list = []
    goals = db.query(Goals).all()
    for item in goals:
        goals_list.append(StaticGoalModel(**item.__dict__))
    res = StaticGoalResponseModel(
        code=status.HTTP_200_OK,
        data=goals_list
    )
    return res

@static_data_router.get('/commitment', response_model=StaticCommitmentResponseModel)
def get_goal_type(db: Session=Depends(get_db)):
    goals_list = []
    goals = db.query(Commitment).all()
    for item in goals:
        goals_list.append(StaticCommitmentModel(**item.__dict__))
    res = StaticCommitmentResponseModel(
        code=status.HTTP_200_OK,
        data=goals_list
    )
    return res