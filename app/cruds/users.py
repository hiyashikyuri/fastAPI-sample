from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate

SECRET_KEY = "b3226dd82a51d689793c805021c665a3b32ee39149fa651af5871af221b45cbd"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password.encode('utf8'), hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password.encode('utf8'))


def authenticate_user(fake_db, username: str, password: str):
    user = find_one(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def find_one(db, username: str):
    return db.query(User).filter(User.username == username).first()


def save(db: Session, user: UserCreate):
    db_user = User(username=user.username, hashed_password=get_password_hash(user.password), email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
