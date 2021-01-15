from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
import shutil

from . import models
from .database import Base
from .models.user import User
from .models.post import Post

from .cruds.posts import create_post, post_list, get_post
from .cruds.users import get_user, create_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from .database import SessionLocal, engine
from .schemas import Token, UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username) シンプルにするために
        token_data = username
    except JWTError:
        raise credentials_exception
    # user = get_user(db, username=token_data.username) シンプルにするために
    user = get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/users/")
def user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create(title: str, body: str, file: UploadFile = File(...), db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    with open("media/" + file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    url = str("media" + file.filename)
    return create_post(db=db, user_id=user_id, title=title, body=body, url=url)


@app.get("/posts/")
def post(db: Session = Depends(get_db)):
    return post_list(db=db)


@app.get("/posts/{post_id}")
def post_detail(post_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    post = get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post does not exists")
    return post
