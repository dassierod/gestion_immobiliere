from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        secret_key = secrets.token_hex(32)
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///gestion_immobiliere.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "warning"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.rooms import rooms_bp
    from .routes.payments import payments_bp
    from .routes.expenses import expenses_bp
    from .routes.parameters import parameters_bp
    from .routes.export import export_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(parameters_bp)
    app.register_blueprint(export_bp)

    with app.app_context():
        db.create_all()
        _seed_defaults()

    return app


def _seed_defaults():
    from .models import Parameter

    defaults = [
        ("loyer_chambre_1", "25000", "Loyer mensuel chambre 1"),
        ("loyer_chambre_2", "25000", "Loyer mensuel chambre 2"),
        ("loyer_chambre_3", "25000", "Loyer mensuel chambre 3"),
        ("hygiene_mensuel", "0", "Charges hygiène mensuel"),
        ("caissier_mensuel", "0", "Frais caissier mensuel"),
    ]
    for key, value, label in defaults:
        if not Parameter.query.filter_by(key=key).first():
            db.session.add(Parameter(key=key, value=value, label=label))
    db.session.commit()
