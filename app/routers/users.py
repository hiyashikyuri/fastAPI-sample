from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from ..database import Base, engine
from ..models.user import User
from ..cruds.users import create_user
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
