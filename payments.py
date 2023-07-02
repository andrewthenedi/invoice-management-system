from flask import Blueprint, request, jsonify
import datetime
from models import db, Payment
from flask_jwt_extended import jwt_required

payments_bp = Blueprint("payments_bp", __name__)


@payments_bp.route("/payment", methods=["POST"])
@jwt_required()
def create_payment():
    data = request.get_json()
    if "amount" not in data or "invoice_id" not in data:
        return jsonify({"message": "Invalid request"}), 400
    new_payment = Payment(
        date=datetime.datetime.now(),
        amount=data["amount"],
        invoice_id=data["invoice_id"],
    )
    db.session.add(new_payment)
    db.session.commit()
    return {"id": new_payment.id}, 201


@payments_bp.route("/payment/<int:id>", methods=["GET"])
@jwt_required()
def get_payment(id):
    payment = Payment.query.get(id)
    if payment is None:
        return jsonify({"message": "Payment not found"}), 404
    return {
        "id": payment.id,
        "date": str(payment.date),
        "amount": payment.amount,
        "invoice_id": payment.invoice_id,
    }


@payments_bp.route("/payment/<int:id>", methods=["PUT"])
@jwt_required()
def update_payment(id):
    payment = Payment.query.get(id)
    if payment is None:
        return jsonify({"message": "Payment not found"}), 404
    data = request.get_json()
    if "amount" in data:
        payment.amount = data["amount"]
    if "invoice_id" in data:
        payment.invoice_id = data["invoice_id"]
    db.session.commit()
    return jsonify({"message": "Payment updated successfully"}), 200


@payments_bp.route("/payment/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_payment(id):
    payment = Payment.query.get(id)
    if payment is None:
        return jsonify({"message": "Payment not found"}), 404
    db.session.delete(payment)
    db.session.commit()
    return jsonify({"message": "Payment deleted successfully"}), 200


@payments_bp.route("/payments", methods=["GET"])
def get_payments():
    all_payments = Payment.query.all()
    return {
        "payments": [
            {
                "id": payment.id,
                "date": str(payment.date),
                "amount": payment.amount,
                "invoice_id": payment.invoice_id,
            }
            for payment in all_payments
        ]
    }
