from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app, get_db
from ..database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        # テスト用のDBに接続するためのsessionmaker instanse
        #  (SessionLocal) をfixtureから受け取る

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        # fixtureから受け取るSessionLocalを使うようにget_dbを強制的に変更
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_dbを元に戻す
        app.dependency_overrides[get_db] = get_db

    return func


client = TestClient(app)
user = {"username": "test", "email": "deadpool@example.com", "password": "chimichangas4life"}
post = {"title": "title", "body": "body", "user_id": None}
import json


def create_user():
    return client.post("/users", json=user)


def create_token():
    return client.post("/token", data={"username": user["username"], "password": user["password"]})


@temp_db
def test_create():
    created_user = create_user().json()
    token = create_token().json()["access_token"]

    post["user_id"] = created_user["id"]

    response = client.post("/posts", data=json.dumps(post), headers={'Authorization': 'Bearer {}'.format(token)})
    print('------')
    print(response.text)
    print(json.dumps(post))
    print('------')

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == post["title"]
    assert "id" in data

#
# @temp_db
# def test_find_one():
#     user = create_user().json()
#     post["user_id"] = user["id"]
#     created_post_data = client.post("/posts", json=post)
#
#     searched_post = client.get("/posts/{post_id}".format(post_id=created_post_data.json()["id"]))
#     assert searched_post.status_code == 200, searched_post.text
#     data = searched_post.json()
#     assert "title" in data
#     assert "body" in data
