from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    """A registered student. UserMixin gives Flask-Login the
    is_authenticated / is_active / get_id() helpers for free."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lost_items = db.relationship("LostItem", backref="reporter", lazy=True, cascade="all, delete-orphan")
    found_items = db.relationship("FoundItem", backref="finder", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Admin(UserMixin, db.Model):
    """Separate table for the campus admin. Kept apart from
    'users' so a compromised student account can never touch
    admin powers, and so the schema matches the spec (4 tables)."""
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def get_id(self):
        # Prefixed so Flask-Login's user_loader can tell a User
        # session apart from an Admin session sharing one login manager.
        return f"admin-{self.id}"

    def __repr__(self):
        return f"<Admin {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("admin-"):
        return Admin.query.get(int(user_id.split("-")[1]))
    return User.query.get(int(user_id))
