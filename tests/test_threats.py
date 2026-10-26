"""Tests for threat CRUD and service layer."""
from app.services.threat_service import create_threat, list_threats, find_matching_threats
from app.extensions import db


def _login(client, app):
    from werkzeug.security import generate_password_hash
    from app.models.analyst import Analyst
    with app.app_context():
        a = Analyst(username="threattester", password_hash=generate_password_hash("password123"))
        db.session.add(a)
        db.session.commit()
    client.post("/auth/login", data={"username": "threattester", "password": "password123"})


def test_create_threat_service(app):
    with app.app_context():
        t = create_threat({
            "threat_name": "TestThreat",
            "threat_type": "Malware",
            "severity": "High",
            "indicator_value": "indicator-1",
            "source": "unit",
            "date_identified": None,
        })
        assert t.threat_id is not None
        assert find_matching_threats("indicator-1") != []


def test_threat_list_page_requires_auth(client):
    r = client.get("/threats/")
    assert r.status_code in (302, 303)


def test_threat_crud_flow(client, app):
    _login(client, app)
    # create
    r = client.post("/threats/new", data={
        "threat_name": "NewThreat",
        "threat_type": "Phishing",
        "severity": "Medium",
        "indicator_value": "ind-2",
        "source": "test",
    }, follow_redirects=True)
    assert r.status_code == 200
    # list
    r = client.get("/threats/")
    assert r.status_code == 200
    assert b"NewThreat" in r.data
