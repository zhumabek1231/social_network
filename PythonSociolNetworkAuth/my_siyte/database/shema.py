from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional,List
from datetime import date,datetime

class UserProfileInputShem(BaseModel):

    first_name:str
    last_name: str
    username: str
    email: EmailStr
    password:str
    phone_number: Optional[str]
    age: int
    is_official: bool


class UserProfileOutShema(BaseModel):
    id:int
    first_name:str
    last_name: str
    username: str
    email: EmailStr
    password:str
    phone_number: Optional[str]
    age: int
    date_registered: date

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CurrentUserSchema (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    username: str
    is_official: bool


