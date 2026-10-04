from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.model import StoriesComment
from mysite.shemas.shemas import StoriesCommentCreate, StoriesCommentUpdate, StoriesCommentOut

router = APIRouter(prefix="/comments", tags=["StoriesComment"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()

@router.post("/", response_model=StoriesCommentOut)
def create_comment(data: StoriesCommentCreate, db: Session = Depends(get_db)):
    comment = StoriesComment(**data.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=list[StoriesCommentOut])
def list_comments(story_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(StoriesComment)
    if story_id is not None:
        query = query.filter(StoriesComment.story == story_id)
    return query.all()


@router.get("/{comment_id}", response_model=StoriesCommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(StoriesComment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=StoriesCommentOut)
def update_comment(comment_id: int, data: StoriesCommentUpdate, db: Session = Depends(get_db)):
    comment = db.get(StoriesComment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(StoriesComment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}