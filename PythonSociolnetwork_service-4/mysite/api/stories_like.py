from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.model import StoriesLike
from mysite.shemas.shemas import StoriesLikeCreate, StoriesLikeUpdate, StoriesLikeOut

router = APIRouter(prefix="/likes", tags=["StoriesLike"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()


@router.post("/", response_model=StoriesLikeOut)
def create_like(data: StoriesLikeCreate, db: Session = Depends(get_db)):
    like = StoriesLike(**data.model_dump())
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


@router.get("/", response_model=list[StoriesLikeOut])
def list_likes(story_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(StoriesLike)
    if story_id is not None:
        query = query.filter(StoriesLike.story == story_id)
    return query.all()


@router.get("/{like_id}", response_model=StoriesLikeOut)
def get_like(like_id: int, db: Session = Depends(get_db)):
    like = db.get(StoriesLike, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return like


@router.put("/{like_id}", response_model=StoriesLikeOut)
def update_like(like_id: int, data: StoriesLikeUpdate, db: Session = Depends(get_db)):
    like = db.get(StoriesLike, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(like, field, value)
    db.commit()
    db.refresh(like)
    return like


@router.delete("/{like_id}")
def delete_like(like_id: int, db: Session = Depends(get_db)):
    like = db.get(StoriesLike, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()
    return {"detail": "Like deleted"}

