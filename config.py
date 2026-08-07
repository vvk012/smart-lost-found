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
