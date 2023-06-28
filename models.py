# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", backref=db.backref("invoices", lazy=True))

    def __repr__(self):
        return f"<Invoice {self.id}>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"))

    invoice = db.relationship("Invoice", backref=db.backref("payments", lazy=True))

    def __repr__(self):
        return f"<Payment {self.id}>"
