"""Tests for public user registration and authentication."""
from werkzeug.security import check_password_hash

from app.extensions import db
from app.models.user import User


def _register(client, email="user@example.com", password="password123", full_name="Test User"):
    return client.post(
        "/users/register",
        data={
            "full_name": full_name,
            "email": email,
            "password": password,
            "confirm_password": password,
        },
        follow_redirects=True,
    )


def test_register_page(client):
    r = client.get("/users/register")
    assert r.status_code == 200
    assert b"Create your account" in r.data


def test_user_registration_success(client, app):
    r = _register(client)
    assert r.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        assert user is not None
        assert user.full_name == "Test User"
        assert user.password_hash != "password123"
        assert check_password_hash(user.password_hash, "password123")



def test_duplicate_email_rejected(client, app):
    _register(client, email="dup@example.com")
    client.post("/users/logout", data={})
    r = _register(client, email="dup@example.com")
    assert r.status_code == 200
    assert b"already exists" in r.data.lower()
    with app.app_context():
        assert User.query.filter_by(email="dup@example.com").count() == 1


def test_duplicate_email_normalized(client, app):
    _register(client, email="Mixed@Example.com")
    client.post("/users/logout", data={})
    r = _register(client, email="mixed@example.com")
    assert b"already exists" in r.data.lower()


def test_invalid_registration_data(client):
    r = client.post(
        "/users/register",
        data={
            "full_name": "A",
            "email": "not-an-email",
            "password": "short",
            "confirm_password": "different",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_password_hashing(client, app):
    _register(client, email="hash@example.com", password="supersecret")
    with app.app_context():
        user = User.query.filter_by(email="hash@example.com").first()
        assert user is not None
        assert "supersecret" not in user.password_hash



def test_login_success(client, app):
    _register(client, email="login@example.com", password="password123")
    client.post("/users/logout", data={})
    r = client.post(
        "/users/login",
        data={"email": "login@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_login_wrong_password(client, app):
    _register(client, email="wrong@example.com", password="password123")
    client.post("/users/logout", data={})
    r = client.post(
        "/users/login",
        data={"email": "wrong@example.com", "password": "notcorrect"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Invalid email or password" in r.data


def test_logout(client, app):
    _register(client, email="logout@example.com", password="password123")
    r = client.post("/users/logout", data={}, follow_redirects=True)
    assert r.status_code == 200
    r2 = client.get("/users/profile")
    assert r2.status_code in (302, 303)
    assert "/users/login" in r2.headers.get("Location", "")


def test_csrf_protection(client, app):
    app.config["WTF_CSRF_ENABLED"] = True
    try:
        r = client.post(
            "/users/register",
            data={
                "full_name": "CSRF User",
                "email": "csrf@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        assert r.status_code in (400, 403)
    finally:
        app.config["WTF_CSRF_ENABLED"] = False



def test_unauthenticated_profile_redirect(client):
    r = client.get("/users/profile")
    assert r.status_code in (302, 303)
    assert "/users/login" in r.headers.get("Location", "")


def test_public_user_blocked_from_analyst_routes(client, app):
    _register(client, email="public@example.com", password="password123")
    for path in ("/analyst/", "/threats/"):
        r = client.get(path)
        assert r.status_code in (302, 303), path
        assert "/auth/login" in r.headers.get("Location", ""), path


def test_report_submission_persists_user(client, app):
    _register(client, email="reporter@example.com", password="password123")
    r = client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="reporter@example.com").first()
        from app.models.report import Report

        report = Report.query.order_by(Report.report_id.desc()).first()
        assert report is not None
        assert report.user_id == user.user_id



def test_analyst_login_visible_when_public_logged_in(client, app):
    _register(client, email="nav@example.com", password="password123")
    r = client.get("/")
    assert r.status_code == 200
    assert b"Analyst Login" in r.data


def test_profile_has_analyst_login(client, app):
    _register(client, email="profilelink@example.com", password="password123")
    r = client.get("/users/profile")
    assert r.status_code == 200
    assert b"Analyst Login" in r.data


def test_database_tables(app):
    from sqlalchemy import inspect
    from app.extensions import db

    with app.app_context():
        tables = set(inspect(db.engine).get_table_names())
        assert {"Users", "Reports", "Analysts", "Threats", "Investigations", "AuditLogs"}.issubset(tables)


def test_init_db_command(runner):
    res = runner.invoke(args=["init-db"])
    assert res.exit_code == 0, res.output






def test_database_persistence_across_requests(client, app):
    _register(client, email="persist@example.com", password="password123")
    client.post("/users/logout", data={})
    r = client.post(
        "/users/login",
        data={"email": "persist@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_migrate_db_command(runner):
    res = runner.invoke(args=["migrate-db"])
    assert res.exit_code == 0, res.output

def test_profile_shows_own_reports(client, app):
    _register(client, email="owner@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    r = client.get("/users/profile")
    assert r.status_code == 200
    assert b"RPT-" in r.data
    assert b"Phishing" in r.data
    assert b"Delete" in r.data


def test_delete_own_report(client, app):
    _register(client, email="deleteowner@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    with app.app_context():
        from app.models.report import Report
        from app.models.user import User

        user = User.query.filter_by(email="deleteowner@example.com").first()
        report = Report.query.filter_by(user_id=user.user_id).first()
        assert report is not None
        report_id = report.report_id

    r = client.get(f"/users/reports/{report_id}/delete")
    assert r.status_code == 200
    assert b"Delete report" in r.data

    r = client.post(f"/users/reports/{report_id}/delete", data={}, follow_redirects=True)
    assert r.status_code == 200
    assert b"deleted successfully" in r.data.lower()
    with app.app_context():
        from app.models.report import Report

        assert Report.query.get(report_id) is None


def test_cannot_delete_other_users_report(client, app):
    _register(client, email="owner2@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    with app.app_context():
        from app.models.report import Report

        report = Report.query.order_by(Report.report_id.desc()).first()
        report_id = report.report_id

    client.post("/users/logout", data={}, follow_redirects=True)
    _register(client, email="other@example.com", password="password123")
    r = client.post(f"/users/reports/{report_id}/delete", data={}, follow_redirects=True)
    assert r.status_code == 200
    with app.app_context():
        from app.models.report import Report

        assert Report.query.get(report_id) is not None


def test_get_does_not_delete_report(client, app):
    _register(client, email="getdelete@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    with app.app_context():
        from app.models.report import Report

        report = Report.query.order_by(Report.report_id.desc()).first()
        report_id = report.report_id

    r = client.get(f"/users/reports/{report_id}/delete")
    assert r.status_code == 200
    with app.app_context():
        from app.models.report import Report

        assert Report.query.get(report_id) is not None


def test_anonymous_cannot_access_delete_report(client):
    r = client.get("/users/reports/1/delete")
    assert r.status_code in (302, 303)
    assert "/users/login" in r.headers.get("Location", "")


def test_delete_csrf_protection(client, app):
    _register(client, email="csrfdelete@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    with app.app_context():
        from app.models.report import Report

        report = Report.query.order_by(Report.report_id.desc()).first()
        report_id = report.report_id


def test_delete_report_removes_investigation(client, app):
    _register(client, email="invowner@example.com", password="password123")
    client.post(
        "/reports/new",
        data={
            "threat_type": "Phishing",
            "indicator_type": "URL",
            "indicator_value": "https://example.com/login",
            "description": "Suspicious phishing email received.",
            "source_context": "email",
        },
        follow_redirects=True,
    )
    with app.app_context():
        from app.models.report import Report
        from app.models.user import User

        user = User.query.filter_by(email="invowner@example.com").first()
        report = Report.query.filter_by(user_id=user.user_id).first()
        report_id = report.report_id

    with app.app_context():
        from app.models.analyst import Analyst
        from werkzeug.security import generate_password_hash
        from app.extensions import db

        analyst = Analyst(username="analystinv", password_hash=generate_password_hash("secret123"))
        db.session.add(analyst)
        db.session.commit()

    client.post("/users/logout", data={}, follow_redirects=True)
    client.post(
        "/auth/login",
        data={"username": "analystinv", "password": "secret123"},
        follow_redirects=True,
    )
    client.post(
        f"/analyst/reports/{report_id}/investigate",
        data={"assessment": "Under Investigation", "investigation_notes": "note"},
        follow_redirects=True,
    )
    client.post("/auth/logout", data={}, follow_redirects=True)
    client.post(
        "/users/login",
        data={"email": "invowner@example.com", "password": "password123"},
        follow_redirects=True,
    )
    r = client.post(f"/users/reports/{report_id}/delete", data={}, follow_redirects=True)
    assert r.status_code == 200
    with app.app_context():
        from app.models.report import Report
        from app.models.investigation import Investigation

        assert Report.query.get(report_id) is None
        assert Investigation.query.filter_by(report_id=report_id).count() == 0

    app.config["WTF_CSRF_ENABLED"] = True
    try:
        r = client.post(f"/users/reports/{report_id}/delete", data={})
        assert r.status_code in (400, 403)
    finally:
        app.config["WTF_CSRF_ENABLED"] = False

