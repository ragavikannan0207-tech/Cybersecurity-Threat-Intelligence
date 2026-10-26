"""Threat intelligence CRUD and search service."""
from app.extensions import db
from app.models.threat import Threat


def create_threat(data):
    threat = Threat(
        threat_name=data["threat_name"].strip(),
        threat_type=data["threat_type"].strip(),
        severity=data["severity"].strip(),
        indicator_value=(data.get("indicator_value") or None),
        source=(data.get("source") or None),
        date_identified=data.get("date_identified"),
    )
    if threat.indicator_value:
        threat.indicator_value = threat.indicator_value.strip() or None
    if threat.source:
        threat.source = threat.source.strip() or None
    db.session.add(threat)
    db.session.commit()
    return threat


def get_threat(threat_id):
    return db.session.get(Threat, threat_id)


def list_threats(page=1, per_page=10, search=None, threat_type=None, indicator=None, sort="date_desc"):
    q = Threat.query
    if search:
        like = f"%{search.strip()}%"
        q = q.filter(Threat.threat_name.ilike(like))
    if threat_type:
        q = q.filter(Threat.threat_type == threat_type.strip())
    if indicator:
        like = f"%{indicator.strip()}%"
        q = q.filter(Threat.indicator_value.ilike(like))
    if sort == "name_asc":
        q = q.order_by(Threat.threat_name.asc())
    elif sort == "name_desc":
        q = q.order_by(Threat.threat_name.desc())
    elif sort == "date_asc":
        q = q.order_by(Threat.date_identified.asc().nullslast() if hasattr(Threat.date_identified, 'asc') else Threat.threat_id.asc())
    else:
        q = q.order_by(Threat.threat_id.desc())
    return q.paginate(page=page, per_page=per_page, error_out=False)


def update_threat(threat, data):
    threat.threat_name = data["threat_name"].strip()
    threat.threat_type = data["threat_type"].strip()
    threat.severity = data["severity"].strip()
    threat.indicator_value = (data.get("indicator_value") or "").strip() or None
    threat.source = (data.get("source") or "").strip() or None
    threat.date_identified = data.get("date_identified")
    db.session.commit()
    return threat


def delete_threat(threat):
    db.session.delete(threat)
    db.session.commit()


def count_threats():
    return Threat.query.count()


def find_matching_threats(indicator_value):
    if not indicator_value:
        return []
    indicator_value = indicator_value.strip()
    return Threat.query.filter(Threat.indicator_value == indicator_value).all()


def all_threat_types():
    rows = db.session.query(Threat.threat_type).distinct().all()
    return sorted({r[0] for r in rows if r[0]})
