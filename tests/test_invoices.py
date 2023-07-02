import unittest
from .test_user import authenticate_user


from models import Invoice


def test_create_invoice(test_client):
    # Authenticate the user
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a new invoice
    invoice_data = {"amount": 1000.00}
    res = test_client.post("/invoice", headers=headers, json=invoice_data)
    assert res.status_code == 201
    assert "id" in res.get_json()


def test_get_invoice(test_client):
    # Authenticate the user
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get an invoice
    res = test_client.get("/invoice/1", headers=headers)
    assert res.status_code == 200
    assert res.json["amount"] == 1000.00


def test_get_invoices(test_client):
    # Authenticate the user
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get all invoices
    res = test_client.get("/invoices", headers=headers)
    assert res.status_code == 200
    assert "invoices" in res.json
    assert len(res.json["invoices"]) > 0


def test_update_invoice(test_client):
    # Authenticate the user
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Update an invoice
    updated_data = {"amount": 1500.00}
    res = test_client.put("/invoice/1", headers=headers, json=updated_data)
    assert res.status_code == 200

    # Get the updated invoice and check if it was indeed updated
    res = test_client.get("/invoice/1", headers=headers)
    assert res.status_code == 200
    assert res.json["amount"] == 1500.00


def test_delete_invoice(test_client):
    # Authenticate the user
    access_token = authenticate_user(test_client, "test", "test123")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Delete an invoice
    res = test_client.delete("/invoice/2", headers=headers)
    assert res.status_code == 200

    # Try to get the deleted invoice, it should return 404
    res = test_client.get("/invoice/2", headers=headers)
    assert res.status_code == 404