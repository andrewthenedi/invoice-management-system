import pytest
from app import create_app, db
from models import User


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        user_data = [
            {"id": 1, "username": "test", "password": "test123", "role": "admin"},
            {"id": 2, "username": "user1", "password": "pass1", "role": "user"},
            {"id": 3, "username": "user2", "password": "pass2", "role": "user"},
        ]
        for data in user_data:
            user = User(username=data["username"], role=data["role"])
            user.set_password(data["password"])
            user.id = data["id"]
            db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def test_client(test_app):
    with test_app.test_request_context():
        with test_app.test_client() as client:
            yield client
