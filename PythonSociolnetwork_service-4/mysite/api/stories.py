from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.model import Stories
from mysite.shemas.shemas import StoriesCreate, StoriesUpdate, StoriesOut

router = APIRouter(prefix="/stories", tags=["Stories"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()


@router.post("/", response_model=StoriesOut)
def create_story(data: StoriesCreate, db: Session = Depends(get_db)):
    story = Stories(**data.model_dump())
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


@router.get("/", response_model=list[StoriesOut])
def list_stories(db: Session = Depends(get_db)):
    return db.query(Stories).all()


@router.get("/{story_id}", response_model=StoriesOut)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.get(Stories, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.put("/{story_id}", response_model=StoriesOut)
def update_story(story_id: int, data: StoriesUpdate, db: Session = Depends(get_db)):
    story = db.get(Stories, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(story, field, value)
    db.commit()
    db.refresh(story)
    return story


@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.get(Stories, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    db.commit()
    db.refresh(story)
    return story


@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.get(Stories, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    db.delete(story)
    db.commit()
    return {"detail": "Story deleted"}