"""Analyst authentication blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash
from app.forms import LoginForm
from app.models.analyst import Analyst

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("analyst_id"):
        return redirect(url_for("analyst.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        analyst = Analyst.query.filter_by(username=form.username.data.strip()).first()
        if analyst and analyst.is_active and check_password_hash(analyst.password_hash, form.password.data):
            session.clear()
            session["analyst_id"] = analyst.analyst_id
            session["analyst_username"] = analyst.username
            session.permanent = True
            flash("Welcome back.", "success")
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("analyst.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("public.index"))
