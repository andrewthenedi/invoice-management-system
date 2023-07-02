# tests.py
import unittest
from app import create_app, db
from models import User


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.user_data = {"username": "test", "password": "test123", "role": "admin"}
        with self.app.app_context():
            db.create_all()
            new_user = User(
                username=self.user_data["username"], role=self.user_data["role"]
            )
            new_user.set_password(self.user_data["password"])
            db.session.add(new_user)
            db.session.commit()

    def test_user_creation(self):
        with self.app.app_context():
            user = User.query.filter_by(username=self.user_data["username"]).first()
            self.assertIsNotNone(user)

    def test_successful_login(self):
        with self.app.app_context():
            res = self.client().post("/login", json=self.user_data)
            self.assertEqual(res.status_code, 200)
            self.assertIn("access_token", res.get_json())

    def test_unsuccessful_login(self):
        incorrect_data = {"username": "wrong", "password": "wrong"}
        res = self.client().post("/login", json=incorrect_data)
        self.assertEqual(res.status_code, 401)

    def test_get_user(self):
        # Login first
        res = self.client().post("/login", json=self.user_data)
        access_token = res.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Get the user
        with self.app.app_context():
            user = User.query.filter_by(username=self.user_data["username"]).first()
            res = self.client().get(f"/user/{user.id}", headers=headers)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json()["username"], self.user_data["username"])

    def test_update_user(self):
        # Login first
        res = self.client().post("/login", json=self.user_data)
        access_token = res.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Update the user
        updated_data = {"username": "updated", "role": "user"}
        with self.app.app_context():
            user = User.query.filter_by(username=self.user_data["username"]).first()
            res = self.client().put(
                f"/user/{user.id}", headers=headers, json=updated_data
            )
            self.assertEqual(res.status_code, 200)

            updated_user = User.query.filter_by(
                username=updated_data["username"]
            ).first()
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.role, updated_data["role"])

    def test_delete_user(self):
        # Login first
        res = self.client().post("/login", json=self.user_data)
        access_token = res.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Delete the user
        with self.app.app_context():
            user = User.query.filter_by(username=self.user_data["username"]).first()
            res = self.client().delete(f"/user/{user.id}", headers=headers)
            self.assertEqual(res.status_code, 200)

            deleted_user = User.query.filter_by(
                username=self.user_data["username"]
            ).first()
            self.assertIsNone(deleted_user)

    def test_non_existent_user(self):
        # Login first
        res = self.client().post("/login", json=self.user_data)
        access_token = res.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Try to get, update, and delete a non-existent user
        with self.app.app_context():
            non_existent_user_id = (
                99999  # Assuming this ID doesn't exist in the database
            )
            res = self.client().get(f"/user/{non_existent_user_id}", headers=headers)
            self.assertEqual(res.status_code, 404)

            updated_data = {"username": "updated", "role": "user"}
            res = self.client().put(
                f"/user/{non_existent_user_id}", headers=headers, json=updated_data
            )
            self.assertEqual(res.status_code, 404)

            res = self.client().delete(f"/user/{non_existent_user_id}", headers=headers)
            self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
