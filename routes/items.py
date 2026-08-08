from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from extensions import db
from models import LostItem, FoundItem
from forms import LostItemForm, FoundItemForm, SearchForm
from utils import save_item_image, send_report_confirmation

items_bp = Blueprint("items", __name__)


@items_bp.route("/report/lost", methods=["GET", "POST"])
@login_required
def report_lost():
    form = LostItemForm()
    if form.validate_on_submit():
        image_filename = save_item_image(form.image.data)
        item = LostItem(
            item_name=form.item_name.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            location_lost=form.location_lost.data.strip(),
            date_lost=form.date_lost.data,
            student_name=form.student_name.data.strip(),
            contact_number=form.contact_number.data.strip(),
            image_filename=image_filename,
            user_id=current_user.id,
        )
        db.session.add(item)
        db.session.commit()

        try:
            send_report_confirmation(current_user.email, current_user.full_name, item.item_name, "lost")
        except Exception:
            pass  # Email is a nice-to-have; never block the user on SMTP issues.

        flash("Lost item reported successfully. We hope you find it soon!", "success")
        return redirect(url_for("items.item_details", item_type="lost", item_id=item.id))

    return render_template("items/report_lost.html", form=form)


@items_bp.route("/report/found", methods=["GET", "POST"])
@login_required
def report_found():
    form = FoundItemForm()
    if form.validate_on_submit():
        image_filename = save_item_image(form.image.data)
        item = FoundItem(
            item_name=form.item_name.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            location_found=form.location_found.data.strip(),
            date_found=form.date_found.data,
            finder_name=form.finder_name.data.strip(),
            contact_number=form.contact_number.data.strip(),
            image_filename=image_filename,
            user_id=current_user.id,
        )
        db.session.add(item)
        db.session.commit()

        try:
            send_report_confirmation(current_user.email, current_user.full_name, item.item_name, "found")
        except Exception:
            pass

        flash("Found item reported successfully. Thank you for helping the campus!", "success")
        return redirect(url_for("items.item_details", item_type="found", item_id=item.id))

    return render_template("items/report_found.html", form=form)


@items_bp.route("/search")
def search():
    form = SearchForm(request.args, meta={"csrf": False})
    lost_results, found_results = [], []

    if request.args:
        keyword = (form.keyword.data or "").strip()
        category = form.category.data
        location = (form.location.data or "").strip()
        status = form.status.data
        item_type = form.item_type.data

        if item_type in ("", "lost"):
            q = LostItem.query
            if keyword:
                q = q.filter(LostItem.item_name.ilike(f"%{keyword}%"))
            if category:
                q = q.filter(LostItem.category == category)
            if location:
                q = q.filter(LostItem.location_lost.ilike(f"%{location}%"))
            if status:
                q = q.filter(LostItem.status == status)
            lost_results = q.order_by(LostItem.created_at.desc()).all()

        if item_type in ("", "found"):
            q = FoundItem.query
            if keyword:
                q = q.filter(FoundItem.item_name.ilike(f"%{keyword}%"))
            if category:
                q = q.filter(FoundItem.category == category)
            if location:
                q = q.filter(FoundItem.location_found.ilike(f"%{location}%"))
            if status:
                q = q.filter(FoundItem.status == status)
            found_results = q.order_by(FoundItem.created_at.desc()).all()

    return render_template("items/search.html", form=form,
                            lost_results=lost_results, found_results=found_results,
                            searched=bool(request.args))


@items_bp.route("/item/<item_type>/<int:item_id>")
def item_details(item_type, item_id):
    if item_type == "lost":
        item = LostItem.query.get_or_404(item_id)
    elif item_type == "found":
        item = FoundItem.query.get_or_404(item_id)
    else:
        abort(404)
    return render_template("items/item_details.html", item=item, item_type=item_type)


@items_bp.route("/my-reports")
@login_required
def my_reports():
    my_lost = LostItem.query.filter_by(user_id=current_user.id).order_by(LostItem.created_at.desc()).all()
    my_found = FoundItem.query.filter_by(user_id=current_user.id).order_by(FoundItem.created_at.desc()).all()
    return render_template("items/my_reports.html", my_lost=my_lost, my_found=my_found)


def _own_lost_item_or_403(item_id):
    item = LostItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    return item


def _own_found_item_or_403(item_id):
    item = FoundItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    return item


@items_bp.route("/my-reports/lost/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_my_lost(item_id):
    item = _own_lost_item_or_403(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'"{item.item_name}" deleted.', "info")
    return redirect(url_for("items.my_reports"))


@items_bp.route("/my-reports/found/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_my_found(item_id):
    item = _own_found_item_or_403(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'"{item.item_name}" deleted.', "info")
    return redirect(url_for("items.my_reports"))


@items_bp.route("/my-reports/lost/<int:item_id>/mark-returned", methods=["POST"])
@login_required
def mark_my_lost_returned(item_id):
    item = _own_lost_item_or_403(item_id)
    item.status = "Returned"
    db.session.commit()
    flash(f'Great news! "{item.item_name}" marked as returned.', "success")
    return redirect(url_for("items.my_reports"))


@items_bp.route("/my-reports/found/<int:item_id>/mark-returned", methods=["POST"])
@login_required
def mark_my_found_returned(item_id):
    item = _own_found_item_or_403(item_id)
    item.status = "Returned"
    db.session.commit()
    flash(f'"{item.item_name}" marked as returned.', "success")
    return redirect(url_for("items.my_reports"))