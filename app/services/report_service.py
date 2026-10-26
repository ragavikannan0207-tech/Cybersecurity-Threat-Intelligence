"""Report submission and retrieval service."""
from datetime import datetime
from app.extensions import db
from app.models.report import Report


def create_report(data):
    report = Report(
        threat_type=data["threat_type"].strip(),
        indicator_type=(data.get("indicator_type") or None),
        indicator_value=(data.get("indicator_value") or None),
        description=data["description"].strip(),
        source_context=(data.get("source_context") or None),
        status="Pending Review",
        user_id=data.get("user_id"),
    )
    if report.indicator_type:
        report.indicator_type = report.indicator_type.strip() or None
    if report.indicator_value:
        report.indicator_value = report.indicator_value.strip() or None
    if report.source_context:
        report.source_context = report.source_context.strip() or None
    db.session.add(report)
    db.session.commit()
    return report


def get_report(report_id):
    return db.session.get(Report, report_id)


def list_reports(page=1, per_page=10, status=None, search=None, user_id=None):
    q = Report.query
    if status and status != "All":
        q = q.filter(Report.status == status)
    if user_id is not None:
        q = q.filter(Report.user_id == user_id)
    if search:
        like = f"%{search.strip()}%"
        q = q.filter(
            db.or_(
                Report.report_id == _safe_int(search),
                Report.indicator_value.ilike(like),
                Report.description.ilike(like),
                Report.threat_type.ilike(like),
                Report.source_context.ilike(like),
            )
        )
    q = q.order_by(Report.reported_at.desc())
    return q.paginate(page=page, per_page=per_page, error_out=False)


def update_report_status(report, status):
    if status not in ["Pending Review", "Under Investigation", "Confirmed Threat", "Unsubstantiated", "Closed"]:
        raise ValueError("Invalid status")
    report.status = status
    db.session.commit()
    return report


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1

def delete_report(report):
    """Permanently delete a user-owned report.

    The Report model's investigation relationship uses cascade delete-orphan,
    so any analyst investigation tied to this report is removed with it. Audit
    log entries are retained as historical records (they have no foreign key to
    Reports) and continue to reference the deleted report ID.
    """
    db.session.delete(report)
    db.session.commit()

