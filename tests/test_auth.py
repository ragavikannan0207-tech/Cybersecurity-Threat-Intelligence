"""Tests for analyst auth and workspace."""
from werkzeug.security import generate_password_hash
from app.models.analyst import Analyst
from app.extensions import db


def _make_analyst(app):
    with app.app_context():
        a = Analyst(username="analyst1", password_hash=generate_password_hash("secret123"))
        db.session.add(a)
        db.session.commit()
        return a.analyst_id


def test_login_page(client):
    r = client.get("/auth/login")
    assert r.status_code == 200


def test_protected_redirect(client):
    r = client.get("/analyst/")
    assert r.status_code in (302, 303)
    assert "/auth/login" in r.headers.get("Location", "")


def test_login_success_and_dashboard(client, app):
    _make_analyst(app)
    r = client.post("/auth/login", data={"username": "analyst1", "password": "secret123"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"workspace" in r.data.lower() or b"Analyst workspace" in r.data


def test_login_failure(client, app):
    _make_analyst(app)
    r = client.post("/auth/login", data={"username": "analyst1", "password": "wrong"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Invalid" in r.data


def test_create_analyst_cli(runner):
    res = runner.invoke(args=["create-analyst", "--username", "cliuser", "--password", "clipass123"])
    # may prompt? options provided, should succeed
    assert res.exit_code == 0, res.output

def test_login_ragavi(client, app):
    from app.models.analyst import Analyst
    from werkzeug.security import generate_password_hash
    from app.extensions import db

    with app.app_context():
        analyst = Analyst(username="ragavi", password_hash=generate_password_hash("test@123"))
        db.session.add(analyst)
        db.session.commit()

    r = client.post("/auth/login", data={"username": "ragavi", "password": "test@123"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"workspace" in r.data.lower() or b"Analyst" in r.data

