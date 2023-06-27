from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


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


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Invoice {self.id}>"


if __name__ == "__main__":
    app.run(debug=True)
