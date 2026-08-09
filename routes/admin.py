from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, bcrypt
from models import Admin, User, LostItem, FoundItem
from forms import AdminLoginForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    """Restricts a route to logged-in Admin accounts only.
    A logged-in *student* hitting an admin URL is redirected to
    the admin login instead of being shown a 403 — friendlier UX
    for a mini-project, while still blocking access either way."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash("Please log in as admin to access this page.", "warning")
            return redirect(url_for("admin.admin_login"))
        return view_func(*args, **kwargs)
    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for("admin.admin_dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        form = AdminLoginForm()
        if form.validate_on_submit():
            print(f"DEBUG >> username received: [{form.username.data}] | password received: [{form.password.data}]")
            admin = Admin.query.filter_by(username=form.username.data.strip()).first()
        admin = Admin.query.filter_by(username=form.username.data.strip()).first()
        if admin and bcrypt.check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            flash("Welcome, Admin.", "success")
            return redirect(url_for("admin.admin_dashboard"))
        flash("Invalid admin credentials.", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def admin_logout():
    logout_user()
    flash("Admin logged out.", "info")
    return redirect(url_for("admin.admin_login"))


@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    stats = {
        "total_users": User.query.count(),
        "total_lost": LostItem.query.count(),
        "total_found": FoundItem.query.count(),
        "returned": (LostItem.query.filter_by(status="Returned").count()
                     + FoundItem.query.filter_by(status="Returned").count()),
        "pending": (LostItem.query.filter_by(status="Pending").count()
                    + FoundItem.query.filter_by(status="Pending").count()),
    }
    recent_lost = LostItem.query.order_by(LostItem.created_at.desc()).limit(5).all()
    recent_found = FoundItem.query.order_by(FoundItem.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats,
                            recent_lost=recent_lost, recent_found=recent_found)


@admin_bp.route("/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/lost-reports")
@admin_required
def admin_lost_reports():
    reports = LostItem.query.order_by(LostItem.created_at.desc()).all()
    return render_template("admin/lost_reports.html", reports=reports)


@admin_bp.route("/found-reports")
@admin_required
def admin_found_reports():
    reports = FoundItem.query.order_by(FoundItem.created_at.desc()).all()
    return render_template("admin/found_reports.html", reports=reports)


@admin_bp.route("/lost/<int:item_id>/delete", methods=["POST"])
@admin_required
def delete_lost(item_id):
    item = LostItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Lost report "{item.item_name}" deleted.', "info")
    return redirect(url_for("admin.admin_lost_reports"))


@admin_bp.route("/found/<int:item_id>/delete", methods=["POST"])
@admin_required
def delete_found(item_id):
    item = FoundItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Found report "{item.item_name}" deleted.', "info")
    return redirect(url_for("admin.admin_found_reports"))


@admin_bp.route("/lost/<int:item_id>/mark-returned", methods=["POST"])
@admin_required
def mark_lost_returned(item_id):
    item = LostItem.query.get_or_404(item_id)
    item.status = "Returned"
    db.session.commit()
    flash(f'"{item.item_name}" marked as returned.', "success")
    return redirect(url_for("admin.admin_lost_reports"))


@admin_bp.route("/found/<int:item_id>/mark-returned", methods=["POST"])
@admin_required
def mark_found_returned(item_id):
    item = FoundItem.query.get_or_404(item_id)
    item.status = "Returned"
    db.session.commit()
    flash(f'"{item.item_name}" marked as returned.', "success")
    return redirect(url_for("admin.admin_found_reports"))
