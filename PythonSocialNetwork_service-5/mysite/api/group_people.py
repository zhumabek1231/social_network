from typing import List,Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.api.dependencies import get_current_user
from mysite.database.db import SessionLocal
from mysite.database.models import Group, GroupPeople
from mysite.database.shemas import (
    GroupPeopleCreate, GroupPeopleResponse,
)

group_people_router = APIRouter(prefix="/group-people", tags=["Group-People"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()




@group_people_router.post("/people", response_model=GroupPeopleResponse)
async def add_member(data: GroupPeopleCreate, current_user: Annotated[dict, Depends(get_current_user)], db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == data.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Мындай группа жок")

    if group.owner != current_user['id']:
        raise HTTPException(status_code=401, detail="Группага адамды ээси гана кошо алат")

    exists = db.query(GroupPeople).filter(
        GroupPeople.group_id == data.group_id,
        GroupPeople.user_id == data.user_id,
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Бул колдонуучу группада коптон бери бар")

    new_member = GroupPeople(**data.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@group_people_router.get("/{group_id}/people", response_model=List[GroupPeopleResponse])
async def list_members(group_id: int, db: Session = Depends(get_db)):
    return db.query(GroupPeople).filter(GroupPeople.group_id == group_id).all()


@group_people_router.delete("/people/{member_id}")
async def remove_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(GroupPeople).filter(GroupPeople.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()
    return {"detail": "Member removed"}