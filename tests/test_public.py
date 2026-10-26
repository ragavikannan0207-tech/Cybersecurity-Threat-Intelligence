"""Smoke tests for public routes."""
from app.extensions import db
from app.models.report import Report
from app.models.user import User


def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"ThreatIntel" in r.data or b"threat" in r.data.lower()


def test_homepage_actions(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"ThreatIntel" in r.data
    assert b'href="/users/login"' in r.data
    assert b'href="/users/register"' in r.data
    assert b'href="/reports/new"' in r.data
    assert b"User Login" in r.data
    assert b"Sign Up" in r.data
    assert b"Report Anonymously" in r.data


def test_analyst_login_visible_when_logged_out(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Analyst Login" in r.data


def test_about(client):
    r = client.get("/about")
    assert r.status_code == 200


def test_report_form_get(client):
    r = client.get("/reports/new")
    assert r.status_code == 200
    assert b"No account is required" in r.data


def test_anonymous_report_submission(client, app):
    data = {
        "threat_type": "Phishing",
        "indicator_type": "URL",
        "indicator_value": "https://example.com/login",
        "description": "Suspicious phishing email received.",
        "source_context": "email",
    }
    r = client.post("/reports/new", data=data, follow_redirects=True)
    assert r.status_code == 200
    assert b"Report submitted" in r.data or b"submitted" in r.data.lower()
    assert b"RPT-" in r.data
    with app.app_context():
        report = Report.query.order_by(Report.report_id.desc()).first()
        assert report is not None
        assert report.user_id is None
        assert report.status == "Pending Review"
        assert User.query.count() == 0


def test_report_submission_and_confirmation(client):
    data = {
        "threat_type": "Phishing",
        "indicator_type": "URL",
        "indicator_value": "https://example.com/login",
        "description": "Suspicious phishing email received.",
        "source_context": "email",
    }
    r = client.post("/reports/new", data=data, follow_redirects=True)
    assert r.status_code == 200
    assert b"submitted" in r.data.lower() or b"confirmation" in r.data.lower() or b"Report submitted" in r.data

def test_homepage_header_no_report_a_threat(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Report a Threat" not in r.data

