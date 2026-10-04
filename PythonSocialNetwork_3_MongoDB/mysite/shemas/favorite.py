from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class FavoriteStatus(str, Enum):
    active = 'active'
    archived = 'archived'

class FavoriteCreate(BaseModel):
    name: str = Field(default="Сохраненное", max_length=50)


class FavoriteUpdateSchema(BaseModel):
    name: str = Field(..., max_length=50)


class FavoriteResponse(BaseModel):
    id: str
    user_id: int
    name: str
    created_at: datetime



class FavoriteItemCreate(BaseModel):
    favorite_id: str
    content_id: int
    status: FavoriteStatus = Field(default=FavoriteStatus.active)


class FavoriteItemResponse(BaseModel):
    id: str
    favorite_id: str
    content_id: str
    status: FavoriteStatus
    created_at: datetime
