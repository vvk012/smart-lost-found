"""
Run once after installing dependencies to create the database
tables and a default admin account:

    python seed.py

Default admin login:
    username: admin
    password: admin123

CHANGE THIS PASSWORD before showing the project to anyone else,
or before deploying it anywhere beyond your own laptop.
"""
from app import create_app
from extensions import db, bcrypt
from models import Admin

app = create_app()

with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(username="vivek@620").first():
        hashed_pw = bcrypt.generate_password_hash("vivek@123").decode("utf-8")
        admin = Admin(username="admin", password_hash=hashed_pw)
        db.session.add(admin)
        db.session.commit()
        print("Default admin created -> username: admin | password: admin123")
    else:
        print("Admin account already exists, skipping.")

    print("Database ready at database/lostfound.db")
