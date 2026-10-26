"""Application configuration loaded from environment variables."""
import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production-please")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://threatuser:threatpass@127.0.0.1:3306/ThreatIntelDB?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # CSRF
    WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", "true").lower() not in ("false", "0", "no")
    WTF_CSRF_TIME_LIMIT = None

    # Pagination
    REPORTS_PER_PAGE = int(os.environ.get("REPORTS_PER_PAGE", "10"))
    THREATS_PER_PAGE = int(os.environ.get("THREATS_PER_PAGE", "10"))

    # Upload/content limits
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
