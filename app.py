# app.py
from flask import Flask, request, jsonify
import datetime

from models import db, Invoice


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/invoice", methods=["POST"])
    def create_invoice():
        data = request.get_json()
        if "amount" not in data:
            return jsonify({"message": "Invalid request"}), 400
        new_invoice = Invoice(date=datetime.datetime.now(), amount=data["amount"])
        db.session.add(new_invoice)
        db.session.commit()
        return {"id": new_invoice.id}, 201

    def get_invoice_or_404(id):
        invoice = Invoice.query.get(id)
        if invoice is None:
            return jsonify({"message": "Invoice not found"}), 404
        return invoice

    @app.route("/invoice/<int:id>", methods=["GET"])
    def get_invoice(id):
        invoice = get_invoice_or_404(id)
        return {"id": invoice.id, "date": str(invoice.date), "amount": invoice.amount}

    @app.route("/invoices", methods=["GET"])
    def get_invoices():
        all_invoices = Invoice.query.all()
        return {
            "invoices": [
                {"id": invoice.id, "date": str(invoice.date), "amount": invoice.amount}
                for invoice in all_invoices
            ]
        }

    @app.route("/invoice/<id>", methods=["PUT"])
    def update_invoice(id):
        invoice = get_invoice_or_404(id)
        data = request.get_json()

        if "amount" in data:
            invoice.amount = data["amount"]

        db.session.commit()

        return jsonify({"message": "Invoice updated successfully"}), 200

    @app.route("/invoice/<id>", methods=["DELETE"])
    def delete_invoice(id):
        invoice = get_invoice_or_404(id)

        db.session.delete(invoice)
        db.session.commit()

        return jsonify({"message": "Invoice deleted successfully"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
