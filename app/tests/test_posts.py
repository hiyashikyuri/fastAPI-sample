import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app, get_db
from ..database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)
client = TestClient(app)


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


# ゆくゆくはこfixtureにまとめたい
def set_authorization():
    user_data = {
        "username": "test",
        "email": "deadpool@example.com",
        "password": "chimichangas4life"
    }
    created_user = client.post("/users", json=user_data).json()
    token = client.post(
        "/token",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    ).json()["access_token"]

    return {
        "user": created_user,
        "access_token": token
    }


@temp_db
def test_find_all():
    credential = set_authorization()
    post = {
        "title": "title",
        "body": "body",
        "user_id": credential["user"]["id"]
    }
    created_post_data = client.post(
        "/posts",
        data=json.dumps(post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    ).json()
    searched_post = client.get(
        "/posts",
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    )
    assert searched_post.status_code == 200, searched_post.text
    data = searched_post.json()
    # TODO, 自分だけのpostsだけにする設定加えたい
    assert created_post_data in data


@temp_db
def test_find_one():
    credential = set_authorization()
    post = {
        "title": "title",
        "body": "body",
        "user_id": credential["user"]["id"]
    }
    created_post_data = client.post(
        "/posts", data=json.dumps(post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    ).json()
    searched_post = client.get(
        "/posts/{post_id}".format(post_id=created_post_data["id"]),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    )
    assert searched_post.status_code == 200, searched_post.text
    data = searched_post.json()
    assert "title" in data
    assert "body" in data


@temp_db
def test_create():
    credential = set_authorization()
    post = {
        "title": "title",
        "body": "body",
        "user_id": credential["user"]["id"]
    }
    response = client.post(
        "/posts", data=json.dumps(post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == post["title"]
    assert "id" in data


@temp_db
def test_update():
    credential = set_authorization()
    post = {
        "title": "title",
        "body": "body",
        "user_id": credential["user"]["id"]
    }
    created_post = client.post(
        "/posts", data=json.dumps(post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    ).json()
    created_post["title"] = "updatetext"
    created_post["body"] = "updatetext"

    response = client.put(
        "/posts/{}".format(created_post["id"]), data=json.dumps(created_post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == created_post["title"]
    assert data["body"] == created_post["body"]


@temp_db
def test_delete():
    credential = set_authorization()
    post = {
        "title": "title",
        "body": "body",
        "user_id": credential["user"]["id"]
    }
    created_post = client.post(
        "/posts", data=json.dumps(post),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    ).json()
    response = client.delete(
        "/posts/{}".format(created_post["id"]),
        headers={
            'Authorization': 'Bearer {}'.format(credential["access_token"])
        }
    )

    assert response.status_code == 200, response.text
