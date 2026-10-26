"""Investigation workflow service."""
from app.extensions import db
from app.models.investigation import Investigation
from app.models.report import Report


def get_or_create_investigation(report_id, analyst_id):
    inv = Investigation.query.filter_by(report_id=report_id).first()
    if inv is None:
        inv = Investigation(report_id=report_id, analyst_id=analyst_id, assessment="Pending Review")
        db.session.add(inv)
        db.session.commit()
    return inv


def save_investigation(report, analyst, assessment, notes):
    inv = Investigation.query.filter_by(report_id=report.report_id).first()
    if inv is None:
        inv = Investigation(report_id=report.report_id, analyst_id=analyst.analyst_id)
        db.session.add(inv)
    inv.analyst_id = analyst.analyst_id
    inv.assessment = assessment
    inv.investigation_notes = (notes or "").strip() or None
    report.status = assessment
    db.session.commit()
    return inv
