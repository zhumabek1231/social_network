from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String,ForeignKey, DateTime
from typing import List
from datetime import  datetime,date
from mysite.database.db import Base



class Stories(Base):
    __tablename__ = "stories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user:Mapped[str] = mapped_column()
    file:Mapped[str] = mapped_column()
    created_date:Mapped[datetime] = mapped_column(DateTime)

class StoriesLike(Base):
    __tablename__ = "stories_like"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user:Mapped[str] = mapped_column()
    story:Mapped[str] = mapped_column()
    like:Mapped[bool]=mapped_column()

class StoriesComment(Base):
    __tablename__ = "stories_comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user:Mapped[str] = mapped_column()
    story:Mapped[str] = mapped_column()
    text:Mapped[str] = mapped_column()