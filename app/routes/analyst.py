"""Analyst workspace blueprint (protected)."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.decorators import login_required, current_analyst
from app.services.report_service import list_reports, get_report, update_report_status
from app.services.investigation_service import get_or_create_investigation, save_investigation
from app.services.threat_service import find_matching_threats, count_threats
from app.services.audit_service import log_action
from app.forms import InvestigationForm, REPORT_STATUSES

analyst_bp = Blueprint("analyst", __name__, url_prefix="/analyst")


@analyst_bp.route("/")
@login_required
def dashboard():
    status = request.args.get("status", "All")
    search = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    pagination = list_reports(page=page, per_page=10, status=status, search=search or None)
    return render_template(
        "analyst/dashboard.html",
        pagination=pagination,
        reports=pagination.items,
        status=status,
        search=search,
        statuses=["All"] + [s[0] for s in REPORT_STATUSES],
    )


@analyst_bp.route("/reports/<int:report_id>")
@login_required
def report_detail(report_id):
    report = get_report(report_id)
    if report is None:
        return render_template("errors/404.html"), 404
    matches = find_matching_threats(report.indicator_value)
    investigation = get_or_create_investigation(report.report_id, current_analyst().analyst_id)
    form = InvestigationForm(obj=investigation) if investigation else InvestigationForm()
    if investigation:
        form.assessment.data = investigation.assessment
        form.investigation_notes.data = investigation.investigation_notes
    audit_entries = []  # loaded below
    from app.models.audit_log import AuditLog
    audit_entries = (
        AuditLog.query.filter_by(target_type="Report", target_id=report.report_id)
        .order_by(AuditLog.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template(
        "analyst/report_detail.html",
        report=report,
        matches=matches,
        investigation=investigation,
        form=form,
        audit_entries=audit_entries,
        statuses=REPORT_STATUSES,
    )


@analyst_bp.route("/reports/<int:report_id>/investigate", methods=["POST"])
@login_required
def investigate(report_id):
    report = get_report(report_id)
    if report is None:
        return render_template("errors/404.html"), 404
    form = InvestigationForm()
    analyst = current_analyst()
    if form.validate_on_submit():
        assessment = form.assessment.data
        notes = form.investigation_notes.data
        save_investigation(report, analyst, assessment, notes)
        log_action(
            analyst.analyst_id,
            action="update_investigation",
            target_type="Report",
            target_id=report.report_id,
            details=f"assessment={assessment}; notes_len={len(notes or '')}",
        )
        flash("Investigation saved.", "success")
    else:
        flash("Please correct the errors in the form.", "danger")
    return redirect(url_for("analyst.report_detail", report_id=report_id))
