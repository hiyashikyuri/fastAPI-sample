from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    id: int
    title: str
    body: str
    user_id: int
    created_date: datetime

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    body: str


class PostUpdate(BaseModel):
    id: int
    title: str
    body: str
