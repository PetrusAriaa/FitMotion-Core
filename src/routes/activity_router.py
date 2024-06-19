from typing import Annotated, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

from ..db import get_db
from ..dto import ActivityResponseModel, ActivityModel
from ..model import Records

from .auth_router import validate_token

activity_router = APIRouter(tags=["Activity_records"])


@activity_router.get('/daily', response_model=ActivityResponseModel)
def get_weekly_activity(session: Annotated[dict[str, Any], Depends(validate_token)],
                        db: Session=Depends(get_db)):
    user_id = session['id']
    row = db.query(Records).where(Records.created_at==date.today() and  Records.fk_user_id==user_id).first()
    
    if row == None:
        _activity = ActivityModel()
        res = ActivityResponseModel(
            code=status.HTTP_200_OK,
            data=_activity
        )
        return res
    activity = ActivityModel(
        walk_min=row.walk_time_min,
        jogging_min=row.jogging_time_min,
        stand_min=row.stand_time_min,
        sit_min=row.sit_time_min,
        downstair_min=row.downstair_time_min,
        upstair_min=row.upstair_time_min
    )
    res = ActivityResponseModel(
        code=status.HTTP_200_OK,
        data=activity
    )
    return res


@activity_router.get('/weekly', response_model=ActivityResponseModel)
def get_weekly_activity(session: Annotated[dict[str, Any], Depends(validate_token)],
                        db: Session=Depends(get_db)):
    user_id = session['id']
    row = db.execute(
        text(
            f"""
                SELECT 
                    fk_user_id,
                    SUM(walk_time_min) AS total_walk_time_min,
                    SUM(jogging_time_min) AS total_jogging_time_min,
                    SUM(stand_time_min) AS total_stand_time_min,
                    SUM(sit_time_min) AS total_sit_time_min,
                    SUM(downstair_time_min) AS total_downstair_time_min,
                    SUM(upstair_time_min) AS total_upstair_time_min
                FROM 
                    records
                WHERE 
                    fk_user_id = '{user_id}'
                    AND created_at >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY 
                    fk_user_id;
            """
        )
    ).first()
    
    if row == None:
        _activity = ActivityModel()
        res = ActivityResponseModel(
            code=status.HTTP_200_OK,
            data=_activity
        )
        return res
    
    _activity = row._asdict()
    activity = ActivityModel(
        walk_min=_activity["total_walk_time_min"],
        jogging_min=_activity["total_jogging_time_min"],
        stand_min=_activity["total_stand_time_min"],
        sit_min=_activity["total_sit_time_min"],
        downstair_min=_activity["total_downstair_time_min"],
        upstair_min=_activity["total_upstair_time_min"]
    )
    
    res = ActivityResponseModel(
        code=status.HTTP_200_OK,
        data=activity
    )
    
    return res


@activity_router.get('/monthly', response_model=ActivityResponseModel)
def get_weekly_activity(session: Annotated[dict[str, Any], Depends(validate_token)],
                        db: Session=Depends(get_db)):
    user_id = session['id']
    row = db.execute(
        text(
            f"""
                SELECT 
                    fk_user_id,
                    SUM(walk_time_min) AS total_walk_time_min,
                    SUM(jogging_time_min) AS total_jogging_time_min,
                    SUM(stand_time_min) AS total_stand_time_min,
                    SUM(sit_time_min) AS total_sit_time_min,
                    SUM(downstair_time_min) AS total_downstair_time_min,
                    SUM(upstair_time_min) AS total_upstair_time_min
                FROM 
                    records
                WHERE 
                    fk_user_id = '{user_id}'
                    AND created_at >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY 
                    fk_user_id;
            """
        )
    ).first()
    
    if row == None:
        _activity = ActivityModel()
        res = ActivityResponseModel(
            code=status.HTTP_200_OK,
            data=_activity
        )
        return res
    
    _activity = row._asdict()
    activity = ActivityModel(
        walk_min=_activity["total_walk_time_min"],
        jogging_min=_activity["total_jogging_time_min"],
        stand_min=_activity["total_stand_time_min"],
        sit_min=_activity["total_sit_time_min"],
        downstair_min=_activity["total_downstair_time_min"],
        upstair_min=_activity["total_upstair_time_min"]
    )
    
    res = ActivityResponseModel(
        code=status.HTTP_200_OK,
        data=activity
    )
    
    return res