"""Investigation record for a report."""
from datetime import datetime
from app.extensions import db


class Investigation(db.Model):
    __tablename__ = "Investigations"

    investigation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey("Reports.report_id", ondelete="CASCADE"), nullable=False, unique=True)
    analyst_id = db.Column(db.Integer, db.ForeignKey("Analysts.analyst_id"), nullable=False)
    assessment = db.Column(db.String(30), nullable=False, default="Pending Review")
    investigation_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    analyst = db.relationship("Analyst", backref="investigations")
