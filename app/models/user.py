"""Public user account."""
from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reports = db.relationship("Report", backref="user", lazy=True)

    def __init__(self, **kwargs):
        if kwargs.get("email"):
            kwargs["email"] = str(kwargs["email"]).strip().lower()
        if kwargs.get("full_name"):
            kwargs["full_name"] = str(kwargs["full_name"]).strip()
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
