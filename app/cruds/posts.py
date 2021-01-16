from sqlalchemy.orm import Session

from ..models.post import Post


def find_all(db):
    return db.query(Post).all()


def find_one(db, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def save(db: Session, user_id: int, title: str, body: str):
    db_post = Post(title=title, body=body, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update(db: Session, post_id: int, title: str, body: str):
    db_post = find_one(db, post_id)
    db_post.title = title
    db_post.body = body
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete(db: Session, post_id: int):
    db_post = find_one(db, post_id)
    db.delete(db_post)
    db.commit()
    return True
