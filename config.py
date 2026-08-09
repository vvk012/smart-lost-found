import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _normalize_db_url(url):
    """Some providers (Render, Heroku-style) hand out URLs starting with
    'postgres://', but modern SQLAlchemy requires 'postgresql://'.
    Also, we installed psycopg (v3), but SQLAlchemy's default dialect
    for a plain 'postgresql://' URL is psycopg2 — so we make the
    driver explicit as 'postgresql+psycopg://' to match what's
    actually installed."""
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Config:
    # Secret key used to sign session cookies and CSRF tokens.
    # In production, always set this via an environment variable.
    SECRET_KEY = os.environ.get("SECRET_KEY", "campus-lost-found-dev-secret-change-me")

    # Uses PostgreSQL if DATABASE_URL is set (e.g. on Render/Neon in
    # production); falls back to a local SQLite file for development.
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL")) or \
        f"sqlite:///{os.path.join(BASE_DIR, 'database', 'lostfound.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Where uploaded item images are stored, and upload limits.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB max upload size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Email settings — used to send report-confirmation emails.
    # Set MAIL_USERNAME / MAIL_PASSWORD as environment variables; never
    # hardcode real credentials in this file.
    # For Gmail: use an "App Password", not your normal password
    # (Google Account -> Security -> App Passwords).
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")
    # If no MAIL_USERNAME is configured, suppress actual sending so the
    # app still works out of the box without crashing on missing creds.
    MAIL_SUPPRESS_SEND = os.environ.get("MAIL_USERNAME") is None