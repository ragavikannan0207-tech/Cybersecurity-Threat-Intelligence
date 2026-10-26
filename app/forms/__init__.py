"""WTForms for the application."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError, Email, EqualTo
import re


INDICATOR_TYPES = [("URL", "URL"), ("IP", "IP address"), ("Domain", "Domain"), ("Hash", "File hash"), ("Other", "Other")]
THREAT_TYPES = [
    "Malware", "Phishing", "Ransomware", "DDoS", "Brute Force",
    "SQL Injection", "Cross-Site Scripting", "Social Engineering",
    "Data Exfiltration", "Other",
]
SEVERITIES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Critical", "Critical")]
REPORT_STATUSES = [
    ("Pending Review", "Pending Review"),
    ("Under Investigation", "Under Investigation"),
    ("Confirmed Threat", "Confirmed Threat"),
    ("Unsubstantiated", "Unsubstantiated"),
    ("Closed", "Closed"),
]


def _safe_text(value):
    if value is None:
        return value
    # Strip control characters; basic XSS hardening is handled by Jinja escaping,
    # but we also remove null bytes and trim.
    return value.replace("\x00", "").strip()


class ThreatForm(FlaskForm):
    threat_name = StringField("Threat name", validators=[DataRequired(), Length(min=2, max=100)])
    threat_type = SelectField("Threat type", choices=[(t, t) for t in THREAT_TYPES], validators=[DataRequired()])
    severity = SelectField("Severity", choices=SEVERITIES, validators=[DataRequired()])
    indicator_value = StringField("Indicator value", validators=[Optional(), Length(max=255)])
    source = StringField("Source", validators=[Optional(), Length(max=100)])
    date_identified = DateField("Date identified", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Save threat")

    def validate_indicator_value(self, field):
        if field.data:
            field.data = _safe_text(field.data)
            if len(field.data) > 255:
                raise ValidationError("Indicator value is too long.")


class ReportForm(FlaskForm):
    threat_type = SelectField("Threat category", choices=[(t, t) for t in THREAT_TYPES], validators=[DataRequired()])
    indicator_type = SelectField("Indicator type", choices=[("", "Select (optional)")] + INDICATOR_TYPES, validators=[Optional()])
    indicator_value = StringField("Indicator value", validators=[Optional(), Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10, max=2000)])
    source_context = StringField("Source / context", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Submit report")

    def validate_description(self, field):
        field.data = _safe_text(field.data)

    def validate_indicator_value(self, field):
        if field.data:
            field.data = _safe_text(field.data)
            # Light format hints (not blocking) for known types
            v = field.data
            if self.indicator_type.data == "IP":
                if not re.match(r"^[0-9a-fA-F:.]+$", v):
                    raise ValidationError("IP address contains invalid characters.")
            if self.indicator_type.data == "Hash":
                if not re.match(r"^[0-9a-fA-F]+$", v):
                    raise ValidationError("File hash should be hexadecimal.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Sign in")



class InvestigationForm(FlaskForm):
    assessment = SelectField("Assessment", choices=REPORT_STATUSES, validators=[DataRequired()])
    investigation_notes = TextAreaField("Investigation notes", validators=[Optional(), Length(max=4000)])
    submit = SubmitField("Save investigation")


class UserRegistrationForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Create account")

    def validate_full_name(self, field):
        field.data = _safe_text(field.data)

    def validate_email(self, field):
        field.data = _safe_text(field.data).lower()
        from app.models.user import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("An account with this email already exists.")


class UserLoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=128)])
    submit = SubmitField("Sign in")

    def validate_email(self, field):
        field.data = _safe_text(field.data).lower()


# Backwards/alternative names used by tests and templates
RegistrationForm = UserRegistrationForm
