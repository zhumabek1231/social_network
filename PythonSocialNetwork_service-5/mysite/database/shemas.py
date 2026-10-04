from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict



class GroupCreate(BaseModel):
    group_name: str



class GroupUpdate(BaseModel):
    group_name: Optional[str] = None


class GroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_name: str
    owner: int
    created_date: datetime



class GroupPeopleCreate(BaseModel):
    group_id: int
    user_id: int


class GroupPeopleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    user_id: int
    created_date: datetime


class GroupDetailResponse(GroupResponse):

    members: List[GroupPeopleResponse] = []
    messages: List[GroupMessageResponse] = []

class GroupMessageCreate(BaseModel):
    group_id: int
    message: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class GroupMessageUpdate(BaseModel):
    message: str


class GroupMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    user_id: int
    message: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    created_date: datetime