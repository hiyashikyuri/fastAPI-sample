from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
import shutil

from .. import models
from ..database import Base
from ..models.user import User
from ..models.post import Post

from ..cruds.posts import create_post, post_list, get_post
from ..cruds.users import get_user, create_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from ..database import SessionLocal, engine
from ..schemas.user import Token, UserCreate

from ..main import get_db, get_current_user

Base.metadata.create_all(bind=engine)

from fastapi import APIRouter


# routingを下記のように記述する
# router = APIRouter(
#     prefix="/items",
#     tags=["items"],
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users/")
def user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
