"""User-submitted report (complaint), not a verified threat."""
from datetime import datetime
from app.extensions import db


REPORT_STATUSES = [
    "Pending Review",
    "Under Investigation",
    "Confirmed Threat",
    "Unsubstantiated",
    "Closed",
]


class Report(db.Model):
    __tablename__ = "Reports"

    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    threat_type = db.Column(db.String(50), nullable=False)
    indicator_type = db.Column(db.String(50), nullable=True)
    indicator_value = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    source_context = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="Pending Review")
    reported_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=True, index=True)

    investigation = db.relationship("Investigation", backref="report", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "threat_type": self.threat_type,
            "indicator_type": self.indicator_type,
            "indicator_value": self.indicator_value,
            "description": self.description,
            "source_context": self.source_context,
            "status": self.status,
            "reported_at": self.reported_at.isoformat() if self.reported_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
