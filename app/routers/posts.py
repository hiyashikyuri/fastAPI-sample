from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..database import Base, engine
from ..models.user import User
from ..cruds import posts
from ..main import get_db, get_current_user, oauth2_scheme
from ..schemas.post import PostCreate, PostUpdate

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/posts")
def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.find_all(db=db)


@router.get("/posts/{post_id}")
def show(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = posts.find_one(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post does not exists")
    return post


@router.post("/posts")
async def create(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.save(db=db, user_id=post.user_id, title=post.title, body=post.body)


@router.put("/posts/{post_id}")
async def update(post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return posts.update(db=db, post_id=post.id, title=post.title, body=post.body)
