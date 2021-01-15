from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import User


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(BaseModel):
    title: str
    body: str
    user_id: int


class PostList(PostBase):
    created_date: Optional[datetime]
    owner_id: int
    user: User

    class Config:
        orm_mode: True
