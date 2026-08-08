"""
Run once after installing dependencies to create the database
tables and a default admin account:

    python seed.py

Admin login:
    username: vivek@620
    password: vivek@123

This is a real credential now — don't commit this file to a public
GitHub repo with the password left in plain text. Keep the repo
private, or move the password to an environment variable before
pushing.
"""
from app import create_app
from extensions import db, bcrypt
from models import Admin

app = create_app()

ADMIN_USERNAME = "vivek@620"
ADMIN_PASSWORD = "vivek@123"

with app.app_context():
    db.create_all()

    existing = Admin.query.filter_by(username=ADMIN_USERNAME).first()
    if not existing:
        hashed_pw = bcrypt.generate_password_hash(ADMIN_PASSWORD).decode("utf-8")
        admin = Admin(username=ADMIN_USERNAME, password_hash=hashed_pw)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created -> username: {ADMIN_USERNAME} | password: {ADMIN_PASSWORD}")
    else:
        print("Admin account already exists, skipping.")

    print("Database ready at database/lostfound.db")