from sqlalchemy.orm import Session

from ..models.post import Post


def create_post(db: Session, user_id: int, title: str, body: str, url: str):
    db_post = Post(title=title, body=body, url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def post_list(db):
    return db.query(Post).all()
