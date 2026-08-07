from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import LostItem, FoundItem

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Public landing page — visible even to logged-out visitors.
    total_lost = LostItem.query.count()
    total_found = FoundItem.query.count()
    total_returned = (LostItem.query.filter_by(status="Returned").count()
                       + FoundItem.query.filter_by(status="Returned").count())
    return render_template("index.html", total_lost=total_lost,
                            total_found=total_found, total_returned=total_returned)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_lost = LostItem.query.count()
    total_found = FoundItem.query.count()
    my_lost = LostItem.query.filter_by(user_id=current_user.id).count()
    my_found = FoundItem.query.filter_by(user_id=current_user.id).count()

    recent_lost = LostItem.query.order_by(LostItem.created_at.desc()).limit(5).all()
    recent_found = FoundItem.query.order_by(FoundItem.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_lost=total_lost, total_found=total_found,
        my_lost=my_lost, my_found=my_found,
        recent_lost=recent_lost, recent_found=recent_found,
    )
