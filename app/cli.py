"""CLI commands for the application."""
import click
from flask.cli import with_appcontext
from sqlalchemy import text, inspect
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Threat, Report, Analyst, User, Investigation, AuditLog  # noqa: F401


def register_cli(app):
    @app.cli.command("create-analyst")
    @click.option("--username", prompt=True, help="Analyst username")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Analyst password")
    @with_appcontext
    def create_analyst(username, password):
        """Create or safely update an analyst account (password is hashed)."""
        username = username.strip()
        if not username:
            raise click.ClickException("Username cannot be empty.")
        existing = Analyst.query.filter_by(username=username).first()
        if existing:
            existing.password_hash = generate_password_hash(password)
            existing.is_active = True
            db.session.commit()
            click.echo(f"Analyst '{username}' password updated successfully.")
            return
        analyst = Analyst(username=username, password_hash=generate_password_hash(password))
        db.session.add(analyst)
        db.session.commit()
        click.echo(f"Analyst '{username}' created successfully.")

    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Create all database tables from the current models."""
        db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("migrate-db")
    @with_appcontext
    def migrate_db():
        """Safely create missing tables and add missing compatibility columns."""
        db.create_all()

        inspector = inspect(db.engine)
        table_names = set(inspector.get_table_names())
        if "Reports" in table_names:
            columns = {column["name"] for column in inspector.get_columns("Reports")}
            if "user_id" not in columns:
                with db.engine.begin() as connection:
                    connection.execute(text("ALTER TABLE Reports ADD COLUMN user_id INTEGER"))
                click.echo("Added Reports.user_id column.")
            try:
                with db.engine.begin() as connection:
                    connection.execute(text("CREATE INDEX IF NOT EXISTS idx_reports_user ON Reports(user_id)"))
            except Exception:
                # Index syntax varies by database; table functionality still works.
                pass

        click.echo("Database migration complete.")
