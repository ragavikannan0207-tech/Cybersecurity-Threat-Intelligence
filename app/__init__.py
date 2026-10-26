"""Cybersecurity Threat Intelligence Database application package."""
import os
import logging
from flask import Flask
from app.config import Config
from app.extensions import db, csrf, migrate


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Configure server-side logging without exposing details to clients
    logging.basicConfig(level=getattr(logging, str(app.config.get("LOG_LEVEL", "INFO")).upper(), logging.INFO))

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.public import public_bp
    from app.routes.reports import reports_bp
    from app.routes.auth import auth_bp
    from app.routes.analyst import analyst_bp
    from app.routes.threats import threats_bp
    from app.routes.users import users_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(analyst_bp)
    app.register_blueprint(threats_bp)
    app.register_blueprint(users_bp)

    # Convenience aliases for common public-auth URLs.
    from app.routes.users import register as user_register, login as user_login, logout as user_logout, profile as user_profile

    app.add_url_rule("/register", "user_register_root", view_func=user_register, methods=["GET", "POST"])
    app.add_url_rule("/signup", "user_signup_root", view_func=user_register, methods=["GET", "POST"])
    app.add_url_rule("/login", "user_login_root", view_func=user_login, methods=["GET", "POST"])
    app.add_url_rule("/logout", "user_logout_root", view_func=user_logout, methods=["POST"])
    app.add_url_rule("/profile", "user_profile_root", view_func=user_profile, methods=["GET"])
    app.add_url_rule("/account", "user_account_root", view_func=user_profile, methods=["GET"])
    app.add_url_rule("/auth/register", "user_auth_register", view_func=user_register, methods=["GET", "POST"])
    app.add_url_rule("/auth/user/login", "user_auth_user_login", view_func=user_login, methods=["GET", "POST"])

    # Template helpers
    from app.template_helpers import register_template_helpers

    register_template_helpers(app)

    # Error handlers
    from app.errors import register_error_handlers

    register_error_handlers(app)

    # CLI commands
    from app.cli import register_cli

    register_cli(app)

    return app
