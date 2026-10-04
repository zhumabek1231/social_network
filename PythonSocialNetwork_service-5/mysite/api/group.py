from typing import List,Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.api.dependencies import get_current_user
from mysite.database.db import SessionLocal
from mysite.database.models import Group,GroupPeople
from mysite.database.shemas import (
    GroupCreate, GroupUpdate, GroupResponse, GroupDetailResponse,
)

group_router = APIRouter(prefix="/group", tags=["Group"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()


@group_router.post("/", response_model=GroupResponse)
async def create_group(data: GroupCreate,current_user: Annotated[dict, Depends(get_current_user)],db: Session = Depends(get_db)):
    group_db = Group(group_name = data.group_name,owner = current_user['id'])
    db.add(group_db)
    db.flush()

    group_people_db = GroupPeople(group_id=group_db.id, user_id=current_user['id'])

    db.add(group_people_db)
    db.commit()
    db.refresh(group_db)

    return group_db


@group_router.get("/", response_model=List[GroupResponse])
async def list_groups( current_user: Annotated[dict, Depends(get_current_user)],db: Session = Depends(get_db)):
    return db.query(Group).join(GroupPeople,Group.id == GroupPeople.id).filter(GroupPeople.user == current_user['id']).all()


@group_router.get("/{group_id}", response_model=GroupDetailResponse)
async def get_group(group_id: int,current_user: Annotated[dict, Depends(get_current_user)] ,db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Not группа жок")

    member = db.query(GroupPeople).filter(GroupPeople.group_id == current_user['id']).first()

    if not member:
        raise HTTPException(status_code=404, detail="Сиз бул группада жоксуз")

    return group


@group_router.put("/group/{group_id}")
def update_group(group_id: int, data: GroupUpdate, current_user: Annotated[dict, Depends(get_current_user)], db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Мындай группа жок")

    if group.owner != current_user['id']:
        raise HTTPException(status_code=400, detail="Группанын ээси гана озгортуу кыла алат")

    group.group_name = data.group_name
    db.commit()
    db.refresh(group)
    return {'message': 'Группанын маалыматы озгорулду'}


@group_router.delete("/{group_id}")
async def delete_group(group_id: int, current_user: Annotated[dict, Depends(get_current_user)],db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Мында группа ")
    if group.owner != current_user['id']:
        raise HTTPException( detail="Группанын ээси гана очуро  алат",status_code=404)
    db.delete(group)
    db.commit()
    return {"message": "Группа очурулду"}



