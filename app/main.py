from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username) シンプルにするために
        token_data = username
    except JWTError:
        raise credentials_exception
    # user = get_user(db, username=token_data.username) シンプルにするために
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/posts/")
def create_post(title: str, body: str, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    user_id = current_user.id
    return crud.create_post(db=db, user_id=user_id, title=title, body=body)


@app.get("/posts/")
def post_list(db: Session = Depends(get_db)):
    return crud.post_list(db=db)


@app.get("/posts/{post_id}")
def post_detail(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id=post_id)

# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
#
#
# @app.post("/items/", response_model=schemas.Item)
# def create_item_for_user(
#         item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
