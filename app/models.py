from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from datetime import datetime
from .database import Base


# TODO, BaseModelを継承させたい
# class BaseModel(Base):
#     """ ベースモデル
#     """
#     __abstract__ = True
#
#     id = Column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#     )
#
#     created_date = Column(DateTime, default=datetime.utcnow())
#
#     created_at = Column(
#         'created_at',
#         TIMESTAMP(timezone=True),
#         server_default=current_timestamp(),
#         nullable=False,
#         comment='登録日時',
#     )
#
#     updated_at = Column(
#         'updated_at',
#         TIMESTAMP(timezone=True),
#         onupdate=current_timestamp(),
#         comment='最終更新日時',
#     )
#
#     @declared_attr
#     def __mapper_args__(cls):
#         """ デフォルトのオーダリングは主キーの昇順
#
#         降順にしたい場合
#         from sqlalchemy import desc
#         # return {'order_by': desc('id')}
#         """
#         return {'order_by': 'id'}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow())
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow())
    is_active = Column(Boolean, default=True)
    title = Column(String)
    body = Column(String)

    owner_id = relationship("User", back_populates="post")
