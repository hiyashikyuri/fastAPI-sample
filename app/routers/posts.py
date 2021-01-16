from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..database import Base, engine
from ..models.user import User
from ..cruds import posts
from ..main import get_db, get_current_user
from ..schemas.post import PostCreate, PostUpdate, PostBase

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/posts", response_model=List[PostBase])
def index(current_user: User = Depends(get_current_user)):
    """queryで出力もOKだが、current_userに紐づいているのでrelationをそのまま出力"""
    return current_user.posts


@router.get("/posts/{post_id}", response_model=PostBase)
async def show(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = posts.find_one(db, post_id=post_id, user_id=current_user.id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post does not exists")
    return post


@router.post("/posts", response_model=PostBase)
async def create(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.save(db=db, user_id=current_user.id, title=post.title, body=post.body)


# TODO, REST fullにしたいのでリンクにid入れてるが、postされるデータを受け取っているので、idは実は使っていない
# 形式的になってるけど、どうしようか迷っている
@router.put("/posts/{post_id}", response_model=PostBase)
async def update(post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.update(db=db, post_id=post.id, title=post.title, body=post.body, user_id=current_user.id)


@router.delete("/posts/{post_id}")
async def delete(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.delete(db=db, post_id=post_id, user_id=current_user.id)
