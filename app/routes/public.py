"""Public pages blueprint."""
from flask import Blueprint, render_template
from app.services.threat_service import count_threats
from app.services.report_service import list_reports

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    try:
        threat_count = count_threats()
    except Exception:
        threat_count = 0
    try:
        report_count = list_reports(page=1, per_page=1).total
    except Exception:
        report_count = 0
    return render_template("public/index.html", threat_count=threat_count, report_count=report_count)


@public_bp.route("/about")
def about():
    return render_template("public/about.html")
