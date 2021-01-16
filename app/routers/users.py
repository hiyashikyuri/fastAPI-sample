from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..database import Base, engine
from ..models.user import User
from ..cruds.users import save
from ..schemas.user import UserCreate

from ..main import get_db, get_current_user

Base.metadata.create_all(bind=engine)

# routingを下記のように記述する
# router = APIRouter(
#     prefix="/items",
#     tags=["items"],
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )

router = APIRouter()


@router.get("/users/me")
async def show(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users")
def create(user: UserCreate, db: Session = Depends(get_db)):
    return save(db=db, user=user)
