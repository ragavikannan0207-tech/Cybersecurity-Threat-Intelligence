"""Public user authentication blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.forms import UserRegistrationForm, UserLoginForm
from app.models.user import User
from app.models.report import Report
from app.services.report_service import delete_report as delete_report_record
from app.decorators import user_login_required, current_user
from flask import current_app

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("users.profile"))

    form = UserRegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                full_name=form.full_name.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("An account with this email already exists.")
            current_app.logger.warning("Duplicate user registration attempt")
            return render_template("users/register.html", form=form), 400

        session.clear()
        session["user_id"] = user.user_id
        session["user_name"] = user.full_name
        session.permanent = True
        flash("Your account has been created successfully.", "success")
        return redirect(url_for("users.profile"))

    return render_template("users/register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("users.profile"))

    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_active and check_password_hash(user.password_hash, form.password.data):
            session.clear()
            session["user_id"] = user.user_id
            session["user_name"] = user.full_name
            session.permanent = True
            flash("Welcome back.", "success")
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for("users.profile"))
        flash("Invalid email or password.", "danger")

    return render_template("users/login.html", form=form)


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    flash("You have been signed out.", "info")
    return redirect(url_for("public.index"))


@users_bp.route("/profile", methods=["GET"])
@users_bp.route("/dashboard", methods=["GET"])
@user_login_required
def profile():
    user = current_user()
    reports = (
        Report.query.filter_by(user_id=user.user_id)
        .order_by(Report.reported_at.desc())
        .all()
        if user
        else []
    )
    return render_template("users/profile.html", user=user, reports=reports)

@users_bp.route("/reports/<int:report_id>/delete", methods=["GET", "POST"])
@user_login_required
def delete_report(report_id):
    user = current_user()
    report = db.session.get(Report, report_id)
    if report is None or report.user_id != (user.user_id if user else None):
        flash("That report could not be found.", "warning")
        return redirect(url_for("users.profile"))

    if request.method == "POST":
        try:
            delete_report_record(report)
            flash("Report deleted successfully.", "success")
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Failed to delete report %s", report_id)
            flash("We could not delete that report. Please try again.", "danger")
        return redirect(url_for("users.profile"))

    return render_template("users/delete_report.html", report=report)

