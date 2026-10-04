from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String,ForeignKey, DateTime
from typing import List
from datetime import  datetime
from my_siyte.database.db import Base



class UserProfile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password:Mapped[str] = mapped_column()
    age : Mapped[int] = mapped_column()
    phone_number:Mapped[str] = mapped_column()
    is_official : Mapped[bool] = mapped_column(default=False)
    # registered_date:Mapped[datetime]=mapped_column(DateTime)
    tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken",back_populates="user")




class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user: Mapped["UserProfile"] = relationship("UserProfile",back_populates="tokens")
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
