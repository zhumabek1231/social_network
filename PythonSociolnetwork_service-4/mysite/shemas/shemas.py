from datetime import datetime
from pydantic import BaseModel, ConfigDict


# ---------- Stories ----------
class StoriesBase(BaseModel):
    user: str
    file: str


class StoriesCreate(StoriesBase):
    pass


class StoriesUpdate(BaseModel):
    user: str | None = None
    file: str | None = None


class StoriesOut(StoriesBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: datetime

# ---------- StoriesLike ----------
class StoriesLikeBase(BaseModel):
    user: str
    story: int
    like: bool = True


class StoriesLikeCreate(StoriesLikeBase):
    pass


class StoriesLikeUpdate(BaseModel):
    like: bool | None = None


class StoriesLikeOut(StoriesLikeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- StoriesComment ----------
class StoriesCommentBase(BaseModel):
    user: str
    story: int
    text: str


class StoriesCommentCreate(StoriesCommentBase):
    pass


class StoriesCommentUpdate(BaseModel):
    text: str | None = None


class StoriesCommentOut(StoriesCommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int




