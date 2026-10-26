"""Threat intelligence record (original Threats table)."""
from datetime import datetime
from app.extensions import db


class Threat(db.Model):
    __tablename__ = "Threats"

    threat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    threat_name = db.Column(db.String(100), nullable=False)
    threat_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    indicator_value = db.Column(db.String(255), unique=True, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    date_identified = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "threat_id": self.threat_id,
            "threat_name": self.threat_name,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "indicator_value": self.indicator_value,
            "source": self.source,
            "date_identified": self.date_identified.isoformat() if self.date_identified else None,
        }
