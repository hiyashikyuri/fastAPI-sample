from sqlalchemy.orm import Session

from ..main import models


def create_post(db: Session, user_id: int, title: str, body: str, url: str):
    db_post = models.Post(title=title, body=body, url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def post_list(db):
    return db.query(models.Post).all()
