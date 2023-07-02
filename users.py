from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint("users_bp", __name__)


def authenticate():
    data = request.get_json()
    print("Request data:", data)  # Debug print statement
    if "username" not in data or "password" not in data:
        return jsonify({"message": "Bad request"}), 400
    user = User.query.filter_by(username=data["username"]).first()
    if user is None or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid username or password"}), 401
    access_token = create_access_token(identity=user.id)
    print("Access token:", access_token)  # Debug print statement
    return jsonify(access_token=access_token), 200


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "username" not in data or "password" not in data or "role" not in data:
        return jsonify({"message": "Invalid request"}), 400
    new_user = User(username=data["username"], role=data["role"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return {"id": new_user.id}, 201


@users_bp.route("/user", methods=["POST"])
@jwt_required()
def create_user():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    if current_user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    if "username" not in data or "password" not in data or "role" not in data:
        return jsonify({"message": "Invalid request"}), 400
    new_user = User(username=data["username"], role=data["role"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return {"id": new_user.id}, 201


@users_bp.route("/user/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = db.session.get(User, id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return {"id": user.id, "username": user.username, "role": user.role}


@users_bp.route("/user/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    if current_user.role != "admin" and current_user.id != id:
        return jsonify({"message": "Unauthorized"}), 403

    user = db.session.get(User, id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if "username" in data:
        user.username = data["username"]
    if "role" in data:
        user.role = data["role"]
    if "password" in data:
        user.set_password(data["password"])
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


@users_bp.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    print("Current User ID:", current_user_id)
    print("Current User:", current_user)

    if current_user.role != "admin" and current_user.id != id:
        return jsonify({"message": "Unauthorized"}), 403

    user = db.session.get(User, id)
    print("User to Delete:", user)
    print("ID to Delete:", id)

    if user is None:
        print("User not found:", id)
        return jsonify({"message": "User not found"}), 404

    print("Deleting user:", user)
    db.session.delete(user)
    db.session.commit()
    print("User deleted successfully:", user)

    return jsonify({"message": "User deleted successfully"}), 200

@users_bp.route("/login", methods=["POST"])
def login():
    return authenticate()
