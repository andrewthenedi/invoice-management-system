from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

    db = SQLAlchemy()
    db.init_app(app)

    class Invoice(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.DateTime, nullable=False)
        amount = db.Column(db.Float, nullable=False)

        def __repr__(self):
            return f"<Invoice {self.id}>"

    with app.app_context():
        db.create_all()

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/invoice", methods=["POST"])
    def create_invoice():
        data = request.get_json()
        new_invoice = Invoice(date=datetime.datetime.now(), amount=data["amount"])
        db.session.add(new_invoice)
        db.session.commit()
        return {"id": new_invoice.id}, 201

    @app.route("/invoice/<int:id>", methods=["GET"])
    def get_invoice(id):
        invoice = Invoice.query.get(id)
        if invoice is None:
            return {"error": "not found"}, 404
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
        invoice = Invoice.query.get(id)

        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404

        data = request.get_json()

        if "amount" in data:
            invoice.amount = data["amount"]

        db.session.commit()

        return jsonify({"message": "Invoice updated successfully"}), 200

    @app.route("/invoice/<id>", methods=["DELETE"])
    def delete_invoice(id):
        invoice = Invoice.query.get(id)

        if not invoice:
            return jsonify({"message": "Invoice not found"}), 404

        db.session.delete(invoice)
        db.session.commit()

        return jsonify({"message": "Invoice deleted successfully"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
