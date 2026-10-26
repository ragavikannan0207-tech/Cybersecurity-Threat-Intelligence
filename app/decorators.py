"""Auth helpers and decorators."""
from functools import wraps
from flask import session, redirect, url_for, flash, request
from app.extensions import db
from app.models.analyst import Analyst
from app.models.user import User


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("analyst_id"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def user_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("users.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def current_analyst():
    aid = session.get("analyst_id")
    if not aid:
        return None
    return db.session.get(Analyst, aid)


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)

