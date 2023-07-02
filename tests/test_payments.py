from .test_user import authenticate_user
from models import Payment


def test_create_payment(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    payment_data = {"amount": 500.00, "invoice_id": 1}
    res = test_client.post("/payment", headers=headers, json=payment_data)
    assert res.status_code == 201
    assert "id" in res.get_json()


def test_get_payment(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    res = test_client.get("/payment/1", headers=headers)
    assert res.status_code == 200
    assert res.json["amount"] == 500.00


def test_get_payments(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    res = test_client.get("/payments", headers=headers)
    assert res.status_code == 200
    assert "payments" in res.json
    assert len(res.json["payments"]) > 0


def test_update_payment(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"amount": 600.00}
    res = test_client.put("/payment/1", headers=headers, json=updated_data)
    assert res.status_code == 200

    res = test_client.get("/payment/1", headers=headers)
    assert res.status_code == 200
    assert res.json["amount"] == 600.00


def test_delete_payment(test_client):
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    res = test_client.delete("/payment/2", headers=headers)
    assert res.status_code == 200

    res = test_client.get("/payment/2", headers=headers)
    assert res.status_code == 404
