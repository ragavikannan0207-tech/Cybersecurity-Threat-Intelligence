"""Threat reporting blueprint (public submission + confirmation)."""
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, session
from app.forms import ReportForm
from app.services.report_service import create_report
from app.services.threat_service import find_matching_threats
from app.extensions import db
from app.decorators import current_user

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/new", methods=["GET", "POST"])
def new_report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            report = create_report({
                "threat_type": form.threat_type.data,
                "indicator_type": form.indicator_type.data,
                "indicator_value": form.indicator_value.data,
                "description": form.description.data,
                "source_context": form.source_context.data,
                "user_id": getattr(current_user(), "user_id", None),
            })
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Failed to save report submission")
            flash("We could not save your report. Please try again.", "danger")
            return render_template("reports/new.html", form=form), 500
        flash("Your report has been submitted successfully.", "success")
        return redirect(url_for("reports.confirmation", report_id=report.report_id))
    return render_template("reports/new.html", form=form)



@reports_bp.route("/<int:report_id>/confirmation")
def confirmation(report_id):
    from app.services.report_service import get_report

    report = get_report(report_id)
    if report is None:
        return render_template("errors/404.html"), 404
    matches = find_matching_threats(report.indicator_value)
    return render_template("reports/confirmation.html", report=report, matches=matches)
