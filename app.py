# app.py
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import datetime
from models import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
    app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        days=1
    )  # 1 day to expiry
    jwt = JWTManager(app)

    db.init_app(app)

    from invoices import invoices_bp
    from users import users_bp
    from payments import payments_bp

    app.register_blueprint(invoices_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(payments_bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error=str(e)), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
