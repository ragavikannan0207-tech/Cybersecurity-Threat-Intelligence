"""Audit logging service."""
from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(analyst_id, action, target_type, target_id=None, details=None):
    entry = AuditLog(
        analyst_id=analyst_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details,
    )
    db.session.add(entry)
    db.session.commit()
    return entry
