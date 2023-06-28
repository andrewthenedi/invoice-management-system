# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Invoice {self.id}>"
