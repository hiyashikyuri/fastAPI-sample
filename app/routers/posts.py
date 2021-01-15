from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
import shutil
from ..database import Base, engine
from ..models.user import User
from ..cruds.posts import create_post, post_list, get_post
from ..main import get_db, get_current_user, oauth2_scheme

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/posts/", status_code=status.HTTP_201_CREATED)
def create(title: str, body: str, file: UploadFile = File(...), db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    with open("media/" + file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    url = str("media" + file.filename)
    return create_post(db=db, user_id=user_id, title=title, body=body, url=url)


@router.get("/posts/")
def post(db: Session = Depends(get_db)):
    return post_list(db=db)


@router.get("/posts/{post_id}")
def post_detail(post_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    post = get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post does not exists")
    return post
