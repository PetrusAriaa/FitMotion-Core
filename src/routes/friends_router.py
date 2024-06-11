from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..utils import validate_uuid

from ..db import get_db

from ..model import FriendsModel


class FriendsRequestModel(BaseModel):
    userId: str
    friendId: str

friends_router = APIRouter(tags=['Friends'])


def __validate_uuids(user_id, friend_id):
    _user_id, user_err = validate_uuid(user_id)
    _friend_id, friend_err = validate_uuid(friend_id)
    if _user_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message":"Invalid id"})
    if _friend_id == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message":"Invalid id"})
    return _user_id, _friend_id


@friends_router.get('/{user_id}')
def get_friend_list(user_id: str):
    print(user_id)
    return {"message": "friend list"}


@friends_router.get('/invite/{friend_id}')
def create_friend_req(friend_id:str, userId:str, db: Session=Depends(get_db)):
    _user_id, _friend_id = __validate_uuids(friend_id, userId)
    _uuid = uuid4()
    friend_req = FriendsModel(
        id = _uuid,
        fk_user_id = _user_id,
        fk_friend_id = _friend_id,
        created_at = datetime.now()
    )
    db.add(friend_req)
    db.commit()
    
    return {"message": str(_uuid)}