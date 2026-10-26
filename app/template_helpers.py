"""Template filters and helpers."""
from app import create_app  # noqa

# Register Jinja filters on the app's template environment.
from flask import current_app


def _register():
    pass


# Filters are registered via init hook below.
def register_template_helpers(app):
    @app.template_filter("fmt_dt")
    def fmt_dt(value):
        if not value:
            return "-"
        try:
            return value.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return str(value)

    @app.template_filter("fmt_date")
    def fmt_date(value):
        if not value:
            return "-"
        try:
            return value.strftime("%Y-%m-%d")
        except Exception:
            return str(value)

    @app.template_filter("report_ref")
    def report_ref(value):
        try:
            return "RPT-{:06d}".format(int(value))
        except (TypeError, ValueError):
            return str(value)

    @app.template_filter("threat_ref")
    def threat_ref(value):
        try:
            return "THR-{:06d}".format(int(value))
        except (TypeError, ValueError):
            return str(value)
