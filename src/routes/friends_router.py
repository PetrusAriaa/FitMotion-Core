from datetime import date
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..model import FriendRequests, Users
from ..routes.auth_router import validate_token


friends_router = APIRouter(tags=['Friends'])


@friends_router.get('/accept', status_code=status.HTTP_201_CREATED)
def accept_friend_req(reqId: int,
                    session: Annotated[dict[str, Any],Depends(validate_token)],
                    db: Session=Depends(get_db)):
    exec_res = db.execute(text(f"SELECT accept_friend_req(:req_id, :user_id, :created_at)"),
                        {
                            "req_id": reqId,
                            "user_id": session['id'],
                            "created_at": date.today()
                        }).first()._asdict()
    db.commit()

    if exec_res['accept_friend_req'] != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid invitation ID")
    return {"message": "Operation finished"}


@friends_router.get('/invite/{friend_username}')
def create_friend_req(friend_username:str, session: Annotated[dict[str, Any], Depends(validate_token)], db: Session=Depends(get_db)):
    friend_data = db.query(Users).where(Users.username == friend_username).first()
    if friend_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    friend_req = FriendRequests(
        fk_user_id = session['id'],
        friend_id = friend_data.id,
        created_at = date.today()
    )
    db.add(friend_req)
    db.commit()
    
    return {"message": "success"}