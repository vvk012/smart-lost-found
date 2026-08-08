import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key used to sign session cookies and CSRF tokens.
    # In production, always set this via an environment variable.
    SECRET_KEY = os.environ.get("SECRET_KEY", "campus-lost-found-dev-secret-change-me")

    # SQLite database stored inside the database/ folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database', 'lostfound.db')}"
    )
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
