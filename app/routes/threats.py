"""Threat intelligence management blueprint (analyst-protected)."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.decorators import login_required, current_analyst
from app.forms import ThreatForm
from app.services.threat_service import (
    create_threat, get_threat, list_threats, update_threat, delete_threat, count_threats, all_threat_types
)
from app.services.audit_service import log_action
from datetime import datetime

threats_bp = Blueprint("threats", __name__, url_prefix="/threats")


@threats_bp.route("/")
@login_required
def list_view():
    search = request.args.get("q", "").strip()
    threat_type = request.args.get("type", "").strip()
    sort = request.args.get("sort", "date_desc")
    page = request.args.get("page", 1, type=int)
    pagination = list_threats(page=page, per_page=10, search=search or None, threat_type=threat_type or None, sort=sort)
    return render_template(
        "threats/list.html",
        pagination=pagination,
        threats=pagination.items,
        search=search,
        threat_type=threat_type,
        sort=sort,
        types=all_threat_types(),
        total=count_threats(),
    )


@threats_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = ThreatForm()
    if form.validate_on_submit():
        try:
            threat = create_threat({
                "threat_name": form.threat_name.data,
                "threat_type": form.threat_type.data,
                "severity": form.severity.data,
                "indicator_value": form.indicator_value.data,
                "source": form.source.data,
                "date_identified": form.date_identified.data,
            })
        except Exception:
            flash("Could not save the threat record. The indicator may already exist.", "danger")
            return render_template("threats/form.html", form=form, mode="new"), 400
        analyst = current_analyst()
        log_action(analyst.analyst_id, "create_threat", "Threat", threat.threat_id, f"name={threat.threat_name}")
        flash("Threat record created.", "success")
        return redirect(url_for("threats.detail", threat_id=threat.threat_id))
    return render_template("threats/form.html", form=form, mode="new")


@threats_bp.route("/<int:threat_id>")
@login_required
def detail(threat_id):
    threat = get_threat(threat_id)
    if threat is None:
        return render_template("errors/404.html"), 404
    return render_template("threats/detail.html", threat=threat)


@threats_bp.route("/<int:threat_id>/edit", methods=["GET", "POST"])
@login_required
def edit(threat_id):
    threat = get_threat(threat_id)
    if threat is None:
        return render_template("errors/404.html"), 404
    form = ThreatForm(obj=threat)
    if form.validate_on_submit():
        try:
            update_threat(threat, {
                "threat_name": form.threat_name.data,
                "threat_type": form.threat_type.data,
                "severity": form.severity.data,
                "indicator_value": form.indicator_value.data,
                "source": form.source.data,
                "date_identified": form.date_identified.data,
            })
        except Exception:
            flash("Could not update the threat record.", "danger")
            return render_template("threats/form.html", form=form, mode="edit", threat=threat), 400
        analyst = current_analyst()
        log_action(analyst.analyst_id, "update_threat", "Threat", threat.threat_id, f"name={threat.threat_name}")
        flash("Threat record updated.", "success")
        return redirect(url_for("threats.detail", threat_id=threat.threat_id))
    return render_template("threats/form.html", form=form, mode="edit", threat=threat)


@threats_bp.route("/<int:threat_id>/delete", methods=["POST"])
@login_required
def delete(threat_id):
    threat = get_threat(threat_id)
    if threat is None:
        return render_template("errors/404.html"), 404
    analyst = current_analyst()
    log_action(analyst.analyst_id, "delete_threat", "Threat", threat.threat_id, f"name={threat.threat_name}")
    try:
        delete_threat(threat)
    except Exception:
        flash("Could not delete the threat record.", "danger")
        return redirect(url_for("threats.detail", threat_id=threat_id))
    flash("Threat record deleted.", "info")
    return redirect(url_for("threats.list_view"))
