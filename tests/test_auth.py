from models import User


def test_user_creation(test_client):
    user = User.query.filter_by(username="test").first()
    assert user is not None


def test_successful_login(test_client):
    res = test_client.post("/login", json={"username": "test", "password": "test123"})
    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_unsuccessful_login(test_client):
    incorrect_data = {"username": "wrong", "password": "wrong"}
    res = test_client.post("/login", json=incorrect_data)
    assert res.status_code == 401
    assert res.json["message"] == "Invalid username or password"
