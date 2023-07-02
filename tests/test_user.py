from models import User


def authenticate_user(client, username, password):
    res = client.post("/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return res.json.get("access_token")


def test_get_user(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    res = test_client.get("/user/1", headers=headers)
    assert res.status_code == 200
    assert res.json["username"] == "test"


def test_non_existent_user(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    non_existent_user_id = 99999

    res = test_client.get(f"/user/{non_existent_user_id}", headers=headers)
    assert res.status_code == 404
    assert res.json["message"] == "User not found"

    updated_data = {"username": "updated", "role": "user"}
    res = test_client.put(
        f"/user/{non_existent_user_id}", headers=headers, json=updated_data
    )
    assert res.status_code == 404
    assert res.json["message"] == "User not found"

    res = test_client.delete(f"/user/{non_existent_user_id}", headers=headers)
    assert res.status_code == 404
    assert res.json["message"] == "User not found"


def test_delete_user(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    res = test_client.delete("/user/2", headers=headers)
    assert res.status_code == 200
    assert res.json["message"] == "User deleted successfully"

    deleted_user = User.query.filter_by(id=2).first()
    assert deleted_user is None


def test_update_user(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"username": "updated", "role": "user"}
    res = test_client.put("/user/1", headers=headers, json=updated_data)
    assert res.status_code == 200
    assert res.json["message"] == "User updated successfully"

    updated_user = User.query.filter_by(username="updated").first()
    assert updated_user is not None
    assert updated_user.role == "user"
