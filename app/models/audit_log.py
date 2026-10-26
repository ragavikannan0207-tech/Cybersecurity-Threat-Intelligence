"""Audit log of analyst actions."""
from datetime import datetime
from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "AuditLogs"

    audit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    analyst_id = db.Column(db.Integer, db.ForeignKey("Analysts.analyst_id", ondelete="SET NULL"), nullable=True)
    action = db.Column(db.String(80), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    analyst = db.relationship("Analyst", backref="audit_logs")
