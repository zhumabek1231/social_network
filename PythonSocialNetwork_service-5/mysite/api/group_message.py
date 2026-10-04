from typing import List,Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.api.dependencies import get_current_user
from mysite.database.db import SessionLocal
from mysite.database.models import Group, GroupPeople, GroupMessage
from mysite.database.shemas import (
    GroupMessageCreate, GroupMessageResponse,GroupMessageUpdate
)

group_message_router = APIRouter(prefix="/group-message", tags=["Group-Message"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()




@group_message_router.post("/message", response_model=GroupMessageResponse)
async def send_message(data: GroupMessageCreate,current_user: Annotated[dict, Depends(get_current_user)] ,db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == data.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Мындай билдируу жок")

    is_member = db.query(GroupPeople).filter(GroupPeople.group_id == data.group_id,GroupPeople.user == current_user['id']).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Колдонуучу бул группада жок")

    new_message = GroupMessage(
        group_id = data.group_id,
        user = current_user['id'],
        message = data.message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@group_message_router.get("/{group_id}/message", response_model=List[GroupMessageResponse])
async def list_messages(group_id: int, current_user: Annotated[dict, Depends(get_current_user)],db: Session = Depends(get_db)):
    member = db.query(GroupPeople).filter(GroupPeople.group_id == group_id,GroupPeople.user == current_user['id']).first()
    if not member:
        raise HTTPException(status_code=404, detail="Сиз бул группада жоксуз")

    all_message = db.query(GroupMessage).filter(GroupMessage.group_id == group_id).order_by(GroupMessage.created_date.asc()).all()
    return all_message


@group_message_router.put("/message/{message_id}")
async def update_message(message_id: int,data:GroupMessageUpdate,current_user: Annotated[dict, Depends(get_current_user)], db: Session = Depends(get_db)):
    message = db.query(GroupMessage).filter(GroupMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if message.user != current_user['id']:
        raise HTTPException(detail="Маалыматтын ээси гана озгортуу кыла алат",status_code=400)

    message.message = data.message

    db.delete(message)
    db.commit()
    return {"message": "билдируу озгорлтулду"}


@group_message_router.delete("/message/{message_id}")
async def delete_message(message_id: int,current_user: Annotated[dict, Depends(get_current_user)], db: Session = Depends(get_db)):
    message = db.query(GroupMessage).filter(GroupMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Мындай билдируу жок")


    if message.user != current_user['id']:
        raise HTTPException(detail="Маалыматтын ээси гана очуруу кыла алат",status_code=400)

    db.delete(message)
    db.commit()
    return {"message": "билдируу очурулду"}