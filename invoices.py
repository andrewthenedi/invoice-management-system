from flask import Blueprint, request, jsonify
import datetime
from models import db, Invoice
from flask_jwt_extended import jwt_required

invoices_bp = Blueprint("invoices_bp", __name__)


# ... all your invoice related endpoints go here ...
@invoices_bp.route("/invoice", methods=["POST"])
@jwt_required()
def create_invoice():
    data = request.get_json()
    if "amount" not in data:
        return jsonify({"message": "Invalid request"}), 400
    new_invoice = Invoice(date=datetime.datetime.now(), amount=data["amount"])
    db.session.add(new_invoice)
    db.session.commit()
    return {"id": new_invoice.id}, 201


def get_invoice_or_404(id):
    invoice = db.session.get(Invoice, id)
    if invoice is None:
        return jsonify({"message": "Invoice not found"}), 404
    return invoice


@invoices_bp.route("/invoice/<int:id>", methods=["GET"])
@jwt_required()
def get_invoice(id):
    invoice_or_error = get_invoice_or_404(id)
    if isinstance(invoice_or_error, tuple):  # This means it's an error response
        return invoice_or_error

    invoice = invoice_or_error
    return {"id": invoice.id, "date": str(invoice.date), "amount": invoice.amount}


@invoices_bp.route("/invoices", methods=["GET"])
def get_invoices():
    all_invoices = Invoice.query.all()
    return {
        "invoices": [
            {"id": invoice.id, "date": str(invoice.date), "amount": invoice.amount}
            for invoice in all_invoices
        ]
    }


@invoices_bp.route("/invoice/<int:id>", methods=["PUT"])
@jwt_required()
def update_invoice(id):
    invoice = get_invoice_or_404(id)
    data = request.get_json()

    if "amount" in data:
        invoice.amount = data["amount"]

    db.session.commit()

    return jsonify({"message": "Invoice updated successfully"}), 200


@invoices_bp.route("/invoice/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_invoice(id):
    invoice = get_invoice_or_404(id)

    db.session.delete(invoice)
    db.session.commit()

    return jsonify({"message": "Invoice deleted successfully"}), 200
