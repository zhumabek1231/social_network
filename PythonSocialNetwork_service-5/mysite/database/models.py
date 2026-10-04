from datetime import datetime
from typing import List, Optional

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mysite.database.db import Base


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(100))
    owner: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    members: Mapped[List['GroupPeople']] = relationship(back_populates='group', cascade='all, delete-orphan')
    messages: Mapped[List['GroupMessage']] = relationship(back_populates='group', cascade='all, delete-orphan')


class GroupPeople(Base):
    __tablename__ = 'group_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
    user_id: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group: Mapped['Group'] = relationship(back_populates='members')


class GroupMessage(Base):
    __tablename__ = 'group_message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
    user_id: Mapped[int] = mapped_column(Integer)

    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    file_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group: Mapped['Group'] = relationship(back_populates='messages')