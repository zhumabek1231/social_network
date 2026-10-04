from fastapi import HTTPException,Depends,APIRouter
from my_siyte.database.model import UserProfile
from my_siyte.database.shema import UserProfileInputShem, UserProfileOutShema
from my_siyte.database.db import  SessionLocal
from sqlalchemy.orm import Session
from typing import List


user_router =  APIRouter(prefix='/user')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/',response_model= UserProfileOutShema)
async  def create_user(user:UserProfileInputShem,db:Session=Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get( '/', response_model=(List[UserProfileOutShema]))
async def list_user (db: Session = Depends (get_db)):
      return db. query (UserProfile). all()


@user_router.get ('/{user_id}/', response_model=UserProfileOutShema)
async def detail_user (user_id: int, db: Session = Depends (get_db)):
    user = db. query (UserProfile). filter (UserProfile.id==user_id). first ()
    if not user:
        raise HTTPException(detail='Мындай id жок',status_code= 400)
    return user
